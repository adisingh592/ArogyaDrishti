"""
SehatSetu - Multi-Tabular Disease (Anemia / Maternal Health / Breast Cancer) Model Training Script
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
from sklearn.preprocessing import StandardScaler, LabelEncoder
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
    os.path.join(PROJECT_ROOT, "organized_datasets", "Hematology", "Anemia", "anemia", "anemia_dataset.csv"),
    os.path.join(PROJECT_ROOT, "organized_datasets", "Obstetrics_Gynecology", "Maternal_Health_Risk", "maternal+health+risk", "Maternal Health Risk Data Set.csv"),
    os.path.join(PROJECT_ROOT, "organized_datasets", "Oncology_Dermatology", "Breast_Cancer", "breast+cancer+wisconsin+diagnostic", "wdbc.data")
]

MODEL_SAVE_DIR = os.path.join(PROJECT_ROOT, "SehatSetu", "models", "tabular", "other")
RESULTS_SAVE_DIR = os.path.join(PROJECT_ROOT, "SehatSetu", "results", "tabular", "other")

os.makedirs(MODEL_SAVE_DIR, exist_ok=True)
os.makedirs(RESULTS_SAVE_DIR, exist_ok=True)


def find_dataset():
    for path in DATASET_CANDIDATES:
        if os.path.exists(path):
            return path
    raise FileNotFoundError("Other tabular dataset not found in organized_datasets.")


# -------------------------------------------------------------
# 2. LOAD DATASET
# -------------------------------------------------------------
def load_data():
    dataset_path = find_dataset()
    print("=" * 60)
    print("SEHATSETU - ADDITIONAL TABULAR DISEASE MODEL TRAINING")
    print("=" * 60)
    print(f"Loading dataset from: {dataset_path}")
    
    if dataset_path.endswith(".data"):
        df = pd.read_csv(dataset_path, header=None)
    else:
        df = pd.read_csv(dataset_path)
        
    print(f"Dataset shape: {df.shape[0]} rows, {df.shape[1]} columns")
    print("\nDataset Sample:")
    print(df.head(3))
    return df, dataset_path


# -------------------------------------------------------------
# 3. PREPROCESS DATA
# -------------------------------------------------------------
def preprocess_data(df, dataset_path):
    print("\n" + "-" * 40)
    print("PREPROCESSING DATA")
    print("-" * 40)
    
    # Anemia dataset
    if "Anaemic" in df.columns or "Anaemia" in df.columns:
        target_col = "Anaemic" if "Anaemic" in df.columns else "Anaemia"
        drop_cols = [c for c in ["Number", "Name", "Unnamed: 7", "Unnamed: 8", "Unnamed: 9", "Unnamed: 10", "Unnamed: 11", "Unnamed: 12", "Unnamed: 13"] if c in df.columns]
        df = df.drop(columns=drop_cols)
        df[target_col] = df[target_col].astype(str).str.strip().apply(lambda x: 1 if x in ["1", "yes", "Yes", "True"] else 0)
        y = df[target_col].values
        X = df.drop(columns=[target_col])
        
    # Maternal Health Risk dataset
    elif "RiskLevel" in df.columns:
        target_col = "RiskLevel"
        le = LabelEncoder()
        y = le.fit_transform(df[target_col].astype(str))
        X = df.drop(columns=[target_col])
        
    # Breast Cancer (WDBC)
    elif dataset_path.endswith("wdbc.data"):
        target_col = 1  # Diagnosis (M/B)
        y = df[target_col].apply(lambda x: 1 if x == "M" else 0).values
        X = df.drop(columns=[0, 1])
        
    else:
        target_col = df.columns[-1]
        le = LabelEncoder()
        y = le.fit_transform(df[target_col].astype(str))
        X = df.drop(columns=[target_col])
        
    # Encode categorical features
    X_encoded = pd.get_dummies(X, drop_first=True)
    feature_names = [str(c) for c in X_encoded.columns]
    
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
        "target_col": str(target_col)
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
    
    model_path = os.path.join(MODEL_SAVE_DIR, "other_model.pkl")
    joblib.dump(best_model, model_path)
    print(f"Saved model to: {model_path}")
    
    preproc_path = os.path.join(MODEL_SAVE_DIR, "other_preprocessor.pkl")
    joblib.dump(preprocessor, preproc_path)
    print(f"Saved preprocessor to: {preproc_path}")
    
    csv_path = os.path.join(RESULTS_SAVE_DIR, "model_comparison.csv")
    results_df.to_csv(csv_path, index=False)
    print(f"Saved comparison to: {csv_path}")
    
    metrics_path = os.path.join(RESULTS_SAVE_DIR, "metrics.txt")
    with open(metrics_path, "w", encoding="utf-8") as f:
        f.write("SEHATSETU - OTHER TABULAR DISEASE METRICS\n")
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
    plt.title(f"Confusion Matrix - {best_model_name}")
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.tight_layout()
    cm_plot_path = os.path.join(RESULTS_SAVE_DIR, "confusion_matrix.png")
    plt.savefig(cm_plot_path, dpi=150)
    plt.close()
    print(f"Saved confusion matrix plot to: {cm_plot_path}")
    print("\nOther tabular disease training workflow completed successfully!")


def main():
    df, dataset_path = load_data()
    X_train, X_test, y_train, y_test, preprocessor = preprocess_data(df, dataset_path)
    results_df, best_model_name, best_model, best_preds = train_and_evaluate(X_train, X_test, y_train, y_test)
    save_artifacts(results_df, best_model_name, best_model, best_preds, y_test, preprocessor)


if __name__ == "__main__":
    main()
