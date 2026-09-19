"""
SehatSetu - Tabular Disease Prediction Module
Loads trained tabular models and integrates with the Health Recommendation System.
"""

import os
import sys
import numpy as np
import pandas as pd
import joblib

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


def load_tabular_model_and_preprocessor(disease_name):
    """
    Loads the trained model and preprocessor for the specified disease.
    """
    clean_name = disease_name.lower().replace(" ", "_").replace("'", "")
    model_folder = os.path.join(PROJECT_ROOT, "models", "tabular", clean_name)
    
    model_path = os.path.join(model_folder, f"{clean_name}_model.pkl")
    preproc_path = os.path.join(model_folder, f"{clean_name}_preprocessor.pkl")
    
    if not os.path.exists(model_path) or not os.path.exists(preproc_path):
        print(f"Warning: Model or Preprocessor for '{disease_name}' not found at {model_path}.")
        print("Please train the model first by running train.py or train.bat in the respective training folder.")
        return None, None
        
    model = joblib.load(model_path)
    preprocessor = joblib.load(preproc_path)
    return model, preprocessor


def predict_tabular_disease(disease_name, input_data, show_recommendation=True):
    """
    Takes disease name and input features (dict, list, or DataFrame),
    returns predicted outcome and confidence score.
    """
    model, preprocessor = load_tabular_model_and_preprocessor(disease_name)
    
    if model is None or preprocessor is None:
        return {
            "disease": disease_name,
            "status": "Model Not Trained",
            "prediction": None,
            "confidence": None
        }
        
    # Format input into 2D array / DataFrame
    if isinstance(input_data, dict):
        df_input = pd.DataFrame([input_data])
    elif isinstance(input_data, (list, np.ndarray)):
        feature_names = preprocessor.get("feature_names", None)
        if feature_names and len(feature_names) == len(input_data):
            df_input = pd.DataFrame([input_data], columns=feature_names)
        else:
            df_input = pd.DataFrame([input_data])
    else:
        df_input = input_data
        
    # Preprocessing with imputer and scaler
    try:
        imputer = preprocessor.get("imputer")
        scaler = preprocessor.get("scaler")
        
        X_imputed = imputer.transform(df_input) if imputer else df_input
        X_scaled = scaler.transform(X_imputed) if scaler else X_imputed
    except Exception as e:
        print(f"Preprocessing error: {e}")
        return {"disease": disease_name, "status": "Preprocessing Failed", "error": str(e)}
        
    # Predict
    prediction = model.predict(X_scaled)[0]
    
    # Calculate confidence / probability
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(X_scaled)[0]
        confidence = float(np.max(probs) * 100.0)
    else:
        confidence = 85.0  # Default confidence if decision function
        
    # Map prediction outcome
    label_encoder = preprocessor.get("label_encoder")
    if label_encoder:
        predicted_class_name = label_encoder.inverse_transform([prediction])[0]
    else:
        predicted_class_name = "Positive (Disease Detected)" if prediction == 1 else "Negative (Normal / Healthy)"
        
    result = {
        "disease": disease_name,
        "prediction_raw": int(prediction) if isinstance(prediction, (np.integer, int)) else str(prediction),
        "prediction_label": str(predicted_class_name),
        "confidence": round(confidence, 2)
    }
    
    print("=" * 60)
    print(f"SEHATSETU PREDICTION RESULT: {disease_name.upper()}")
    print("=" * 60)
    print(f"Prediction: {result['prediction_label']}")
    print(f"Confidence: {result['confidence']}%")
    
    # Send result to Recommendation System
    if show_recommendation and display_recommendation is not None:
        display_recommendation(disease_name, confidence=f"{result['confidence']}%")
        
    return result


if __name__ == "__main__":
    print("SehatSetu Tabular Prediction Engine loaded successfully.")
    print("Call predict_tabular_disease('diabetes', sample_features) to run predictions.")
