"""
SehatSetu - Medical Image Disease Prediction Module
Loads trained deep learning vision models and connects to the Health Recommendation System.
"""

import os
import sys
import numpy as np

# Setup paths to access recommendation module
def get_project_root():
    curr = os.path.dirname(os.path.abspath(__file__))
    while curr and os.path.dirname(curr) != curr:
        if os.path.exists(os.path.join(curr, "organized_datasets")):
            return curr
        curr = os.path.dirname(curr)
    return os.path.abspath(r"E:\multidisease prdiction")

PROJECT_ROOT = get_project_root()
SEHATSETU_DIR = os.path.join(PROJECT_ROOT, "SehatSetu")
RECOMMENDATION_DIR = os.path.join(SEHATSETU_DIR, "recommendation")

if RECOMMENDATION_DIR not in sys.path:
    sys.path.append(RECOMMENDATION_DIR)

try:
    from recommendation_system import display_recommendation
except ImportError:
    display_recommendation = None


def load_image_model(disease_name):
    """
    Loads the trained Keras/TensorFlow vision model for the specified disease.
    """
    import tensorflow as tf
    clean_name = disease_name.lower().replace(" ", "_").replace("'", "")
    model_path = os.path.join(PROJECT_ROOT, "models", "image", clean_name, f"{clean_name}_model.keras")
    
    if not os.path.exists(model_path):
        print(f"Warning: Model for '{disease_name}' not found at {model_path}.")
        print("Please train the image model first by running train.py or train.bat in the respective image training folder.")
        return None
        
    model = tf.keras.models.load_model(model_path)
    return model


def predict_image_disease(disease_name, image_path, class_names=None, show_recommendation=True):
    """
    Preprocesses the medical image, feeds it to the trained MobileNetV2 model,
    and returns predicted disease category + confidence score.
    """
    import tensorflow as tf
    
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found at path: {image_path}")
        
    model = load_image_model(disease_name)
    if model is None:
        return {
            "disease": disease_name,
            "status": "Model Not Trained",
            "prediction": None,
            "confidence": None
        }
        
    # Load and resize image to 224x224
    img = tf.keras.utils.load_img(image_path, target_size=(224, 224))
    img_array = tf.keras.utils.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Shape (1, 224, 224, 3)
    
    # Model inference
    preds = model.predict(img_array, verbose=0)
    
    # Binary vs Multiclass classification
    if preds.shape[-1] == 1:
        prob = float(preds[0][0])
        confidence = float(prob * 100.0) if prob > 0.5 else float((1.0 - prob) * 100.0)
        default_classes = ["Normal / Uninfected", "Positive Condition Detected"]
        class_list = class_names if class_names else default_classes
        predicted_label = class_list[1] if prob > 0.5 else class_list[0]
    else:
        probs = preds[0]
        pred_idx = int(np.argmax(probs))
        confidence = float(probs[pred_idx] * 100.0)
        if class_names and len(class_names) == len(probs):
            predicted_label = class_names[pred_idx]
        else:
            predicted_label = f"Class_{pred_idx}"
            
    result = {
        "disease": disease_name,
        "image_path": image_path,
        "prediction_label": str(predicted_label),
        "confidence": round(confidence, 2)
    }
    
    print("=" * 60)
    print(f"SEHATSETU IMAGE INFERENCE RESULT: {disease_name.upper()}")
    print("=" * 60)
    print(f"Prediction: {result['prediction_label']}")
    print(f"Confidence: {result['confidence']}%")
    
    # Send result to Recommendation System
    if show_recommendation and display_recommendation is not None:
        display_recommendation(disease_name, confidence=f"{result['confidence']}%")
        
    return result


if __name__ == "__main__":
    print("SehatSetu Medical Image Prediction Engine loaded successfully.")
    print("Call predict_image_disease('pneumonia', 'sample_xray.png') to run image predictions.")
