"""
SehatSetu - Chronic Kidney Disease Model Training Script
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
    os.path.join(PROJECT_ROOT, "organized_datasets", "Renal_System", "Chronic_Kidney_Disease", "Chronic_Kidney_Disease", "chronic_kidney_disease.arff"),
    os.path.join(PROJECT_ROOT, "organized_datasets", "Renal_System", "Chronic_Kidney_Disease", "Chronic_Kidney_Disease", "chronic_kidney_disease_full.arff")
]

MODEL_SAVE_DIR = os.path.join(PROJECT_ROOT, "SehatSetu", "models", "tabular", "kidney_disease")
RESULTS_SAVE_DIR = os.path.join(PROJECT_ROOT, "SehatSetu", "results", "tabular", "kidney_disease")

os.makedirs(MODEL_SAVE_DIR, exist_ok=True)
os.makedirs(RESULTS_SAVE_DIR, exist_ok=True)


def find_dataset():
    for path in DATASET_CANDIDATES:
        if os.path.exists(path):
            return path
    raise FileNotFoundError("Kidney disease dataset not found in organized_datasets.")


# -------------------------------------------------------------
# 2. LOAD AND PARSE ARFF DATASET
# -------------------------------------------------------------
def load_arff_data(filepath):
    attributes = []
    data_rows = []
    is_data = False
    
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line_str = line.strip()
            if not line_str or line_str.startswith("%"):
                continue
            if line_str.lower().startswith("@attribute"):
                parts = line_str.split()
                attr_name = parts[1].strip("'\"")
                attributes.append(attr_name)
            elif line_str.lower().startswith("@data"):
                is_data = True
            elif is_data:
                row = [item.strip() for item in line_str.split(",")]
                if len(row) == len(attributes):
                    data_rows.append(row)
                    
    df = pd.DataFrame(data_rows, columns=attributes)
    df.replace("?", np.nan, inplace=True)
    df.replace("\t?", np.nan, inplace=True)
    return df


def load_data():
    dataset_path = find_dataset()
    print("=" * 60)
    print("SEHATSETU - CHRONIC KIDNEY DISEASE MODEL TRAINING")
    print("=" * 60)
    print(f"Loading dataset from: {dataset_path}")
    
    df = load_arff_data(dataset_path)
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
    
    # Target column is 'class'
    target_col = "class" if "class" in df.columns else df.columns[-1]
    
    # Clean target: 'ckd', 'notckd', 'ckd\t'
    df[target_col] = df[target_col].astype(str).str.strip().str.lower()
    df = df[df[target_col].isin(["ckd", "notckd"])].copy()
    y = df[target_col].apply(lambda x: 1 if x == "ckd" else 0).values
    
    X = df.drop(columns=[target_col])
    
    # Convert numerical columns
    for col in X.columns:
        try:
            converted = pd.to_numeric(X[col], errors="coerce")
            # If mostly numeric, keep converted numeric series
            if converted.notna().sum() > len(X) * 0.3:
                X[col] = converted
        except Exception:
            pass
        
    # One-hot encode categorical features or map them
    X_encoded = pd.get_dummies(X, drop_first=True)
    feature_names = list(X_encoded.columns)
    
    # Impute missing values
    imputer = SimpleImputer(strategy="median")
    X_imputed = imputer.fit_transform(X_encoded)
    
    # Scale features
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
    model_path = os.path.join(MODEL_SAVE_DIR, "kidney_disease_model.pkl")
    joblib.dump(best_model, model_path)
    print(f"Saved model to: {model_path}")
    
    # 2. Save Preprocessor
    preproc_path = os.path.join(MODEL_SAVE_DIR, "kidney_disease_preprocessor.pkl")
    joblib.dump(preprocessor, preproc_path)
    print(f"Saved preprocessor to: {preproc_path}")
    
    # 3. Save Model Comparison CSV
    csv_path = os.path.join(RESULTS_SAVE_DIR, "model_comparison.csv")
    results_df.to_csv(csv_path, index=False)
    print(f"Saved comparison to: {csv_path}")
    
    # 4. Save Metrics Text Report
    metrics_path = os.path.join(RESULTS_SAVE_DIR, "metrics.txt")
    with open(metrics_path, "w", encoding="utf-8") as f:
        f.write("SEHATSETU - CHRONIC KIDNEY DISEASE METRICS\n")
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
    sns.heatmap(cm, annot=True, fmt="d", cmap="Purples", cbar=False)
    plt.title(f"Confusion Matrix - {best_model_name} (Kidney Disease)")
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.tight_layout()
    cm_plot_path = os.path.join(RESULTS_SAVE_DIR, "confusion_matrix.png")
    plt.savefig(cm_plot_path, dpi=150)
    plt.close()
    print(f"Saved confusion matrix plot to: {cm_plot_path}")
    print("\nChronic Kidney Disease training workflow completed successfully!")


def main():
    df = load_data()
    X_train, X_test, y_train, y_test, preprocessor = preprocess_data(df)
    results_df, best_model_name, best_model, best_preds = train_and_evaluate(X_train, X_test, y_train, y_test)
    save_artifacts(results_df, best_model_name, best_model, best_preds, y_test, preprocessor)


if __name__ == "__main__":
    main()
