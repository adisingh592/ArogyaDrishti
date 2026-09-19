"""
SehatSetu - Stroke Prediction Model Training Script
Tabular Classification: Logistic Regression, Decision Tree, Random Forest, SVM
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# -------------------------------------------------------------
# 1. SETUP PATHS
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
    os.path.join(PROJECT_ROOT, "organized_datasets", "Cardiovascular", "Stroke", "heart stroke", "healthcare-dataset-stroke-data.csv")
]

MODEL_SAVE_DIR = os.path.join(PROJECT_ROOT, "SehatSetu", "models", "tabular", "stroke")
RESULTS_SAVE_DIR = os.path.join(PROJECT_ROOT, "SehatSetu", "results", "tabular", "stroke")

os.makedirs(MODEL_SAVE_DIR, exist_ok=True)
os.makedirs(RESULTS_SAVE_DIR, exist_ok=True)


def find_dataset():
    for path in DATASET_CANDIDATES:
        if os.path.exists(path):
            return path
    raise FileNotFoundError("Stroke dataset not found in organized_datasets.")


# -------------------------------------------------------------
# 2. LOAD DATASET
# -------------------------------------------------------------
def load_data():
    dataset_path = find_dataset()
    print("=" * 60)
    print("SEHATSETU - STROKE PREDICTION MODEL TRAINING")
    print("=" * 60)
    print(f"Loading dataset from: {dataset_path}")
    
    df = pd.read_csv(dataset_path)
    print(f"Dataset shape: {df.shape[0]} rows, {df.shape[1]} columns")
    print("\nDataset Sample:")
    print(df.head(3))
    return df


# -------------------------------------------------------------
# 3. PREPROCESS DATA
# -------------------------------------------------------------
def preprocess_data(df):
    print("\n" + "-" * 40)
    print("PREPROCESSING DATA")
    print("-" * 40)
    
    # Drop irrelevant id column if present
    if "id" in df.columns:
        df = df.drop(columns=["id"])
        
    target_col = "stroke" if "stroke" in df.columns else df.columns[-1]
    y = df[target_col].astype(int).values
    X = df.drop(columns=[target_col])
    
    # Convert categorical features using get_dummies
    X_encoded = pd.get_dummies(X, drop_first=True)
    feature_names = list(X_encoded.columns)
    
    # Impute missing values (e.g. bmi has missing values)
    imputer = SimpleImputer(strategy="median")
    X_imputed = imputer.fit_transform(X_encoded)
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_imputed)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Train samples: {len(X_train)}, Test samples: {len(X_test)}")
    
    preprocessor = {
        "scaler": scaler,
        "imputer": imputer,
        "feature_names": feature_names,
        "target_col": target_col
    }
    
    return X_train, X_test, y_train, y_test, preprocessor


# -------------------------------------------------------------
# 4. TRAIN AND EVALUATE MODELS
# -------------------------------------------------------------
def train_and_evaluate(X_train, X_test, y_train, y_test):
    print("\n" + "-" * 40)
    print("TRAINING MODELS")
    print("-" * 40)
    
    # Use class_weight='balanced' to handle stroke class imbalance
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42),
        "Decision Tree": DecisionTreeClassifier(max_depth=5, class_weight="balanced", random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=8, class_weight="balanced", random_state=42),
        "Support Vector Machine": SVC(kernel="rbf", probability=True, class_weight="balanced", random_state=42)
    }
    
    results_list = []
    trained_models = {}
    
    for name, model in models.items():
        print(f"Training {name}...")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average="weighted", zero_division=0)
        rec = recall_score(y_test, y_pred, average="weighted", zero_division=0)
        f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)
        
        results_list.append({
            "Model": name,
            "Accuracy": round(acc, 4),
            "Precision": round(prec, 4),
            "Recall": round(rec, 4),
            "F1-Score": round(f1, 4)
        })
        trained_models[name] = (model, y_pred)
        
    results_df = pd.DataFrame(results_list)
    print("\nModel Comparison Table:")
    print(results_df.to_string(index=False))
    
    best_row = results_df.sort_values(by="F1-Score", ascending=False).iloc[0]
    best_model_name = best_row["Model"]
    best_model, best_preds = trained_models[best_model_name]
    
    print(f"\n>>> Best Model: {best_model_name} (F1-Score: {best_row['F1-Score']})")
    return results_df, best_model_name, best_model, best_preds


# -------------------------------------------------------------
# 5. SAVE ARTIFACTS AND PLOTS
# -------------------------------------------------------------
def save_artifacts(results_df, best_model_name, best_model, best_preds, y_test, preprocessor):
    print("\n" + "-" * 40)
    print("SAVING MODELS AND RESULTS")
    print("-" * 40)
    
    model_path = os.path.join(MODEL_SAVE_DIR, "stroke_model.pkl")
    joblib.dump(best_model, model_path)
    print(f"Saved model to: {model_path}")
    
    preproc_path = os.path.join(MODEL_SAVE_DIR, "stroke_preprocessor.pkl")
    joblib.dump(preprocessor, preproc_path)
    print(f"Saved preprocessor to: {preproc_path}")
    
    csv_path = os.path.join(RESULTS_SAVE_DIR, "model_comparison.csv")
    results_df.to_csv(csv_path, index=False)
    print(f"Saved comparison to: {csv_path}")
    
    metrics_path = os.path.join(RESULTS_SAVE_DIR, "metrics.txt")
    with open(metrics_path, "w", encoding="utf-8") as f:
        f.write("SEHATSETU - STROKE PREDICTION METRICS\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Best Model: {best_model_name}\n\n")
        f.write("Model Comparison:\n")
        f.write(results_df.to_string(index=False) + "\n\n")
        f.write("Classification Report for Best Model:\n")
        f.write(classification_report(y_test, best_preds) + "\n")
    print(f"Saved metrics report to: {metrics_path}")
    
    cm = confusion_matrix(y_test, best_preds)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False)
    plt.title(f"Confusion Matrix - {best_model_name} (Stroke)")
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.tight_layout()
    cm_plot_path = os.path.join(RESULTS_SAVE_DIR, "confusion_matrix.png")
    plt.savefig(cm_plot_path, dpi=150)
    plt.close()
    print(f"Saved confusion matrix plot to: {cm_plot_path}")
    print("\nStroke training workflow completed successfully!")


def main():
    df = load_data()
    X_train, X_test, y_train, y_test, preprocessor = preprocess_data(df)
    results_df, best_model_name, best_model, best_preds = train_and_evaluate(X_train, X_test, y_train, y_test)
    save_artifacts(results_df, best_model_name, best_model, best_preds, y_test, preprocessor)


if __name__ == "__main__":
    main()
