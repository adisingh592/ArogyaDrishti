"""
SehatSetu - Heart Disease Model Training Script
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
    os.path.join(PROJECT_ROOT, "organized_datasets", "Cardiovascular", "Heart_Disease", "heart+failure+clinical+records (1)", "heart_failure_clinical_records_dataset.csv"),
    os.path.join(PROJECT_ROOT, "organized_datasets", "Cardiovascular", "Heart_Disease", "heart+disease", "processed.cleveland.data"),
    os.path.join(PROJECT_ROOT, "organized_datasets", "Cardiovascular", "Heart_Disease", "statlog+heart (1)", "heart.dat")
]

MODEL_SAVE_DIR = os.path.join(PROJECT_ROOT, "SehatSetu", "models", "tabular", "heart_disease")
RESULTS_SAVE_DIR = os.path.join(PROJECT_ROOT, "SehatSetu", "results", "tabular", "heart_disease")

os.makedirs(MODEL_SAVE_DIR, exist_ok=True)
os.makedirs(RESULTS_SAVE_DIR, exist_ok=True)


def find_dataset():
    for path in DATASET_CANDIDATES:
        if os.path.exists(path):
            return path
    raise FileNotFoundError("Heart disease dataset not found in organized_datasets.")


# -------------------------------------------------------------
# 2. LOAD AND INSPECT DATASET
# -------------------------------------------------------------
def load_data():
    dataset_path = find_dataset()
    print("=" * 60)
    print("SEHATSETU - HEART DISEASE MODEL TRAINING")
    print("=" * 60)
    print(f"Loading dataset from: {dataset_path}")
    
    if dataset_path.endswith(".csv"):
        df = pd.read_csv(dataset_path)
    else:
        # Processed UCI heart data format (14 columns)
        cols = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal", "target"]
        try:
            df = pd.read_csv(dataset_path, header=None, names=cols, na_values="?")
        except Exception:
            df = pd.read_csv(dataset_path, delim_whitespace=True, header=None, names=cols, na_values="?")
            
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
    
    # Identify target column
    if "DEATH_EVENT" in df.columns:
        target_col = "DEATH_EVENT"
    elif "target" in df.columns:
        target_col = "target"
        # Binarize if multi-class (0 = no disease, >0 = disease)
        df[target_col] = df[target_col].apply(lambda x: 1 if x > 0 else 0)
    elif "heart_disease" in df.columns:
        target_col = "heart_disease"
    else:
        target_col = df.columns[-1]
        
    X = df.drop(columns=[target_col])
    y = df[target_col].astype(int)
    
    # Impute missing values with median
    imputer = SimpleImputer(strategy="median")
    X_imputed = imputer.fit_transform(X)
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_imputed)
    
    feature_names = list(X.columns)
    
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
    
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Decision Tree": DecisionTreeClassifier(max_depth=5, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42),
        "Support Vector Machine": SVC(kernel="rbf", probability=True, random_state=42)
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
    
    # 1. Save Best Model
    model_path = os.path.join(MODEL_SAVE_DIR, "heart_disease_model.pkl")
    joblib.dump(best_model, model_path)
    print(f"Saved model to: {model_path}")
    
    # 2. Save Preprocessor
    preproc_path = os.path.join(MODEL_SAVE_DIR, "heart_disease_preprocessor.pkl")
    joblib.dump(preprocessor, preproc_path)
    print(f"Saved preprocessor to: {preproc_path}")
    
    # 3. Save Model Comparison CSV
    csv_path = os.path.join(RESULTS_SAVE_DIR, "model_comparison.csv")
    results_df.to_csv(csv_path, index=False)
    print(f"Saved comparison to: {csv_path}")
    
    # 4. Save Metrics Text Report
    metrics_path = os.path.join(RESULTS_SAVE_DIR, "metrics.txt")
    with open(metrics_path, "w", encoding="utf-8") as f:
        f.write("SEHATSETU - HEART DISEASE CLASSIFICATION METRICS\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Best Model: {best_model_name}\n\n")
        f.write("Model Comparison:\n")
        f.write(results_df.to_string(index=False) + "\n\n")
        f.write("Classification Report for Best Model:\n")
        f.write(classification_report(y_test, best_preds) + "\n")
    print(f"Saved metrics report to: {metrics_path}")
    
    # 5. Save Confusion Matrix Plot
    cm = confusion_matrix(y_test, best_preds)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Reds", cbar=False)
    plt.title(f"Confusion Matrix - {best_model_name} (Heart Disease)")
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.tight_layout()
    cm_plot_path = os.path.join(RESULTS_SAVE_DIR, "confusion_matrix.png")
    plt.savefig(cm_plot_path, dpi=150)
    plt.close()
    print(f"Saved confusion matrix plot to: {cm_plot_path}")
    print("\nHeart Disease training workflow completed successfully!")


def main():
    df = load_data()
    X_train, X_test, y_train, y_test, preprocessor = preprocess_data(df)
    results_df, best_model_name, best_model, best_preds = train_and_evaluate(X_train, X_test, y_train, y_test)
    save_artifacts(results_df, best_model_name, best_model, best_preds, y_test, preprocessor)


if __name__ == "__main__":
    main()
