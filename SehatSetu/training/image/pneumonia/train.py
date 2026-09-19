"""
SehatSetu - Pneumonia Detection Model Training Script
Deep Learning Transfer Learning: MobileNetV2
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from sklearn.metrics import classification_report, confusion_matrix

# -------------------------------------------------------------
# 1. SETUP PATHS & HYPERPARAMETERS
# -------------------------------------------------------------
def get_project_root():
    curr = os.path.dirname(os.path.abspath(__file__))
    while curr and os.path.dirname(curr) != curr:
        if os.path.exists(os.path.join(curr, "organized_datasets")):
            return curr
        curr = os.path.dirname(curr)
    return os.path.abspath(r"E:\multidisease prdiction")

PROJECT_ROOT = get_project_root()

DATASET_CANDIDATES = [
    os.path.join(PROJECT_ROOT, "organized_datasets", "Respiratory", "Pneumonia"),
    os.path.join(PROJECT_ROOT, "organized_datasets", "Respiratory", "chest_xray"),
    os.path.join(PROJECT_ROOT, "organized_datasets", "Respiratory", "Tuberculosis", "TB_Chest_Radiography_Database")
]

MODEL_SAVE_DIR = os.path.join(PROJECT_ROOT, "SehatSetu", "models", "image", "pneumonia")
RESULTS_SAVE_DIR = os.path.join(PROJECT_ROOT, "SehatSetu", "results", "image", "pneumonia")

os.makedirs(MODEL_SAVE_DIR, exist_ok=True)
os.makedirs(RESULTS_SAVE_DIR, exist_ok=True)

IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 10
LEARNING_RATE = 0.0001


def find_dataset():
    for path in DATASET_CANDIDATES:
        if os.path.exists(path):
            return path
    # Return first candidate if not found yet
    return DATASET_CANDIDATES[0]


# -------------------------------------------------------------
# 2. LOAD DATASET PIPELINE
# -------------------------------------------------------------
def load_datasets(dataset_path):
    print("=" * 60)
    print("SEHATSETU - PNEUMONIA IMAGE CLASSIFIER TRAINING")
    print("=" * 60)
    print(f"Loading image dataset from: {dataset_path}")
    
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset directory does not exist: {dataset_path}")
        
    train_ds = tf.keras.utils.image_dataset_from_directory(
        dataset_path,
        validation_split=0.2,
        subset="training",
        seed=42,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE
    )
    
    val_ds = tf.keras.utils.image_dataset_from_directory(
        dataset_path,
        validation_split=0.2,
        subset="validation",
        seed=42,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE
    )
    
    class_names = train_ds.class_names
    print(f"\nDiscovered classes ({len(class_names)}): {class_names}")
    
    # Configure dataset for performance
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
    
    return train_ds, val_ds, class_names


# -------------------------------------------------------------
# 3. BUILD TRANSFER LEARNING MODEL (MobileNetV2)
# -------------------------------------------------------------
def build_model(num_classes):
    print("\n" + "-" * 40)
    print("BUILDING MOBILENETV2 ARCHITECTURE")
    print("-" * 40)
    
    # Preprocessing layer (Rescale pixel values 0-255 to 0-1)
    rescale = layers.Rescaling(1.0 / 255.0)
    
    # Data Augmentation for robust generalization
    data_augmentation = tf.keras.Sequential([
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.1),
        layers.RandomZoom(0.1)
    ])
    
    base_model = MobileNetV2(
        input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3),
        include_top=False,
        weights="imagenet"
    )
    base_model.trainable = False  # Freeze pretrained weights
    
    inputs = tf.keras.Input(shape=(IMG_SIZE[0], IMG_SIZE[1], 3))
    x = rescale(inputs)
    x = data_augmentation(x)
    x = base_model(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(128, activation="relu")(x)
    x = layers.Dropout(0.2)(x)
    
    if num_classes == 2:
        outputs = layers.Dense(1, activation="sigmoid")(x)
        loss = "binary_crossentropy"
    else:
        outputs = layers.Dense(num_classes, activation="softmax")(x)
        loss = "sparse_categorical_crossentropy"
        
    model = models.Model(inputs=inputs, outputs=outputs)
    
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE),
        loss=loss,
        metrics=["accuracy"]
    )
    
    model.summary()
    return model


# -------------------------------------------------------------
# 4. TRAIN AND EVALUATE MODEL
# -------------------------------------------------------------
def train_and_evaluate(model, train_ds, val_ds, class_names):
    print("\n" + "-" * 40)
    print("STARTING MODEL TRAINING")
    print("-" * 40)
    
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS
    )
    
    print("\n" + "-" * 40)
    print("EVALUATING MODEL ON VALIDATION SET")
    print("-" * 40)
    
    y_true = []
    y_pred = []
    
    for images, labels in val_ds:
        preds = model.predict(images, verbose=0)
        if len(class_names) == 2:
            preds_labels = (preds > 0.5).astype(int).flatten()
        else:
            preds_labels = np.argmax(preds, axis=1)
            
        y_true.extend(labels.numpy())
        y_pred.extend(preds_labels)
        
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    return history, y_true, y_pred


# -------------------------------------------------------------
# 5. SAVE ARTIFACTS AND PLOTS
# -------------------------------------------------------------
def save_artifacts(model, history, y_true, y_pred, class_names):
    print("\n" + "-" * 40)
    print("SAVING MODEL AND EVALUATION RESULTS")
    print("-" * 40)
    
    # 1. Save Model
    model_save_path = os.path.join(MODEL_SAVE_DIR, "pneumonia_model.keras")
    model.save(model_save_path)
    print(f"Saved model to: {model_save_path}")
    
    # 2. Save Metrics Report
    metrics_path = os.path.join(RESULTS_SAVE_DIR, "metrics.txt")
    with open(metrics_path, "w", encoding="utf-8") as f:
        f.write("SEHATSETU - PNEUMONIA MODEL EVALUATION METRICS\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Architecture: MobileNetV2 Transfer Learning\n")
        f.write(f"Classes: {class_names}\n\n")
        f.write("Classification Report:\n")
        f.write(classification_report(y_true, y_pred, target_names=class_names) + "\n")
    print(f"Saved metrics report to: {metrics_path}")
    
    # 3. Save Confusion Matrix Plot
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=class_names, yticklabels=class_names)
    plt.title("Confusion Matrix - MobileNetV2 (Pneumonia)")
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.tight_layout()
    cm_plot_path = os.path.join(RESULTS_SAVE_DIR, "confusion_matrix.png")
    plt.savefig(cm_plot_path, dpi=150)
    plt.close()
    print(f"Saved confusion matrix plot to: {cm_plot_path}")
    
    # 4. Save Training History Plot
    plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)
    plt.plot(history.history["accuracy"], label="Train Accuracy")
    plt.plot(history.history["val_accuracy"], label="Val Accuracy")
    plt.title("Training and Validation Accuracy")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(history.history["loss"], label="Train Loss")
    plt.plot(history.history["val_loss"], label="Val Loss")
    plt.title("Training and Validation Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend()
    
    plt.tight_layout()
    history_plot_path = os.path.join(RESULTS_SAVE_DIR, "training_history.png")
    plt.savefig(history_plot_path, dpi=150)
    plt.close()
    print(f"Saved training history curves to: {history_plot_path}")
    print("\nPneumonia image training workflow completed successfully!")


def main():
    dataset_path = find_dataset()
    train_ds, val_ds, class_names = load_datasets(dataset_path)
    model = build_model(len(class_names))
    history, y_true, y_pred = train_and_evaluate(model, train_ds, val_ds, class_names)
    save_artifacts(model, history, y_true, y_pred, class_names)


if __name__ == "__main__":
    main()
