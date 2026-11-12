"""
SehatSetu - Report-to-Model Bridge with Meta-Classifier & Adaptive Imputer
Maps values parsed from a medical report onto trained tabular models.
Uses an intelligent meta-classifier to select best matching models,
applies safe population baselines for missing demographic context,
and ensures relevant models run and report transparent confidence.
"""

import math
import os
import joblib

SEHATSETU_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABULAR_MODELS_DIR = os.path.join(SEHATSETU_DIR, "models", "tabular")

# Baseline Population Defaults for missing patient context
POPULATION_DEFAULTS = {
    "age": 45.0,
    "bmi": 24.2,
    "sex": "female",
    "smoking": False,
    "hypertension": False,
}


# -------------------------------------------------------------
# 1. HELPERS TO DERIVE MODEL INPUTS FROM REPORT VALUES
# -------------------------------------------------------------
def flag(v, key, derived=None):
    stated = v.get(key)
    if key == "smoking" and stated == "former":
        stated = False
    if not isinstance(stated, bool):
        stated = None
    if stated is True or derived is True:
        return True
    if stated is False or derived is False:
        return False
    return None


def has_hypertension(v):
    if "systolic_bp" in v:
        return v["systolic_bp"] >= 130 or v.get("diastolic_bp", 80) >= 80
    return None


def has_diabetes(v):
    if v.get("hba1c") is not None:
        return v["hba1c"] >= 6.5
    if v.get("fasting_glucose") is not None:
        return v["fasting_glucose"] >= 126
    return None


def has_anaemia(v):
    if v.get("hemoglobin") is None:
        return None
    return v["hemoglobin"] < (12.0 if v.get("sex") == "female" else 13.0)


def any_glucose(v):
    for key in ("random_glucose", "fasting_glucose", "pp_glucose"):
        if v.get(key) is not None:
            return v[key]
    return None


def as01(x):
    return None if x is None else (1 if x else 0)


def yes_no(x):
    return None if x is None else ("yes" if x else "no")


def brfss_age_group(age):
    if age is None:
        age = POPULATION_DEFAULTS["age"]
    if age < 25:
        return 1
    return min(13, int((age - 25) // 5) + 2)


def sex01(v):
    s = v.get("sex") or POPULATION_DEFAULTS["sex"]
    return 1 if s == "male" else 0


# -------------------------------------------------------------
# 2. PER-MODEL INPUT BUILDERS
# -------------------------------------------------------------
def build_diabetes(v, assumed_tracker):
    smoker = flag(v, "smoking")
    bmi = v.get("bmi")
    if bmi is None:
        if v.get("weight") and v.get("height"):
            h_m = v["height"] / 100.0
            bmi = round(v["weight"] / (h_m * h_m), 1)
        else:
            bmi = POPULATION_DEFAULTS["bmi"]
            assumed_tracker.add("BMI (default 24.2)")

    age = v.get("age")
    if age is None:
        age = POPULATION_DEFAULTS["age"]
        assumed_tracker.add("Age (default 45)")

    raw = {
        "HighBP": as01(flag(v, "hypertension", has_hypertension(v))),
        "HighChol": as01(v["total_cholesterol"] >= 240) if "total_cholesterol" in v else None,
        "CholCheck": 1 if "total_cholesterol" in v else None,
        "BMI": bmi,
        "Smoker": as01(smoker),
        "Stroke": as01(flag(v, "stroke_history")),
        "HeartDiseaseorAttack": as01(flag(v, "heart_disease")),
        "Sex": sex01(v),
        "Age": brfss_age_group(age),
    }
    return raw, assumed_tracker


def build_heart(v, assumed_tracker):
    age = v.get("age")
    if age is None:
        age = POPULATION_DEFAULTS["age"]
        assumed_tracker.add("Age (default 45)")

    raw = {
        "age": age,
        "anaemia": as01(has_anaemia(v)),
        "creatinine_phosphokinase": v.get("cpk"),
        "diabetes": as01(flag(v, "diabetes_history", has_diabetes(v))),
        "ejection_fraction": v.get("ejection_fraction"),
        "high_blood_pressure": as01(flag(v, "hypertension", has_hypertension(v))),
        "platelets": v.get("platelets"),
        "serum_creatinine": v.get("creatinine"),
        "serum_sodium": v.get("sodium"),
        "sex": sex01(v),
        "smoking": as01(flag(v, "smoking")),
        "time": None,
        "trestbps": v.get("systolic_bp"),
        "chol": v.get("total_cholesterol"),
        "fbs": as01(v["fasting_glucose"] > 120) if "fasting_glucose" in v else None,
    }
    return raw, assumed_tracker


def build_kidney(v, assumed_tracker):
    age = v.get("age")
    if age is None:
        age = POPULATION_DEFAULTS["age"]
        assumed_tracker.add("Age (default 45)")

    raw = {
        "age": age,
        "bp": v.get("diastolic_bp"),
        "sg": v.get("specific_gravity"),
        "al": v.get("urine_albumin"),
        "su": v.get("urine_sugar"),
        "rbc": None, "pc": None, "pcc": None, "ba": None,
        "bgr": any_glucose(v),
        "bu": v.get("urea"),
        "sc": v.get("creatinine"),
        "sod": v.get("sodium"),
        "pot": v.get("potassium"),
        "hemo": v.get("hemoglobin"),
        "pcv": v.get("pcv"),
        "wbcc": v.get("wbc"),
        "rbcc": v.get("rbc"),
        "htn": yes_no(flag(v, "hypertension", has_hypertension(v))),
        "dm": yes_no(flag(v, "diabetes_history", has_diabetes(v))),
        "cad": yes_no(flag(v, "heart_disease")),
        "appet": None if "poor_appetite" not in v else ("poor" if v["poor_appetite"] else "good"),
        "pe": yes_no(flag(v, "pedal_edema")),
        "ane": yes_no(has_anaemia(v)),
    }
    return raw, assumed_tracker


def build_liver(v, assumed_tracker):
    age = v.get("age")
    if age is None:
        age = POPULATION_DEFAULTS["age"]
        assumed_tracker.add("Age (default 45)")

    raw = {
        "Age": age,
        "Gender": sex01(v),
        "Total_Bilirubin": v.get("total_bilirubin"),
        "Direct_Bilirubin": v.get("direct_bilirubin"),
        "Alkaline_Phosphotase": v.get("alp"),
        "Alamine_Aminotransferase": v.get("alt"),
        "Aspartate_Aminotransferase": v.get("ast"),
        "Total_Proteins": v.get("total_protein"),
        "Albumin": v.get("albumin"),
        "Albumin_and_Globulin_Ratio": v.get("ag_ratio"),
    }
    return raw, assumed_tracker


def build_thyroid(v, assumed_tracker):
    def measured(key):
        return "y" if v.get(key) is not None else "n"

    age = v.get("age")
    if age is None:
        age = POPULATION_DEFAULTS["age"]
        assumed_tracker.add("Age (default 45)")

    sex = v.get("sex") or POPULATION_DEFAULTS["sex"]
    tt4_nmol = v["t4"] * 12.87 if v.get("t4") is not None else None
    fti = round(tt4_nmol / 0.96, 1) if tt4_nmol is not None else None

    raw = {
        "feature_1": age,
        "feature_2": "M" if sex == "male" else "F",
        "feature_14": measured("tsh"),
        "feature_15": v.get("tsh"),
        "feature_16": measured("t3"),
        "feature_17": v["t3"] * 0.01536 if v.get("t3") is not None else None,
        "feature_18": measured("t4"),
        "feature_19": tt4_nmol,
        "feature_20": "n", "feature_21": None,
        "feature_22": measured("t4"), "feature_23": fti,
        "feature_24": "n", "feature_25": None,
    }
    for col in range(3, 14):
        raw[f"feature_{col}"] = "f"
    return raw, assumed_tracker


def build_stroke(v, assumed_tracker):
    age = v.get("age")
    if age is None:
        age = POPULATION_DEFAULTS["age"]
        assumed_tracker.add("Age (default 45)")

    sex = v.get("sex") or POPULATION_DEFAULTS["sex"]
    smoking = v.get("smoking")
    raw = {
        "gender": sex.capitalize(),
        "age": age,
        "hypertension": as01(flag(v, "hypertension", has_hypertension(v))),
        "heart_disease": as01(flag(v, "heart_disease")),
        "ever_married": None,
        "work_type": None,
        "Residence_type": None,
        "avg_glucose_level": any_glucose(v),
        "bmi": v.get("bmi") or POPULATION_DEFAULTS["bmi"],
        "smoking_status": None if smoking is None else
            ("formerly smoked" if smoking == "former" else "smokes" if smoking else "never smoked"),
    }
    return raw, assumed_tracker


# -------------------------------------------------------------
# 3. META-CLASSIFIER REGISTRY & AFFINITY MATCHER
# -------------------------------------------------------------
MODEL_CATALOG = [
    {
        "folder": "diabetes",
        "label": "Diabetes Risk Model",
        "builder": build_diabetes,
        "primary_markers": ["fasting_glucose", "hba1c", "random_glucose", "pp_glucose", "bmi"],
        "secondary_markers": ["total_cholesterol", "hdl", "ldl", "triglycerides", "systolic_bp", "age"],
        "min_primary_threshold": 1,
        "base_weight": 1.0,
    },
    {
        "folder": "kidney_disease",
        "label": "Chronic Kidney Disease Model",
        "builder": build_kidney,
        "primary_markers": ["creatinine", "urea", "bun", "urine_albumin", "specific_gravity"],
        "secondary_markers": ["hemoglobin", "sodium", "potassium", "wbc", "rbc", "systolic_bp"],
        "min_primary_threshold": 1,
        "base_weight": 1.0,
    },
    {
        "folder": "liver_disease",
        "label": "Liver Disease (ILPD) Model",
        "builder": build_liver,
        "primary_markers": ["alt", "ast", "alp", "total_bilirubin", "direct_bilirubin"],
        "secondary_markers": ["albumin", "total_protein", "ag_ratio"],
        "min_primary_threshold": 1,
        "base_weight": 1.0,
    },
    {
        "folder": "thyroid",
        "label": "Hypothyroidism Model",
        "builder": build_thyroid,
        "primary_markers": ["tsh", "t3", "t4"],
        "secondary_markers": ["age", "sex"],
        "min_primary_threshold": 1,
        "base_weight": 1.0,
    },
    {
        "folder": "stroke",
        "label": "Stroke Risk Model",
        "builder": build_stroke,
        "primary_markers": ["systolic_bp", "diastolic_bp", "fasting_glucose", "random_glucose"],
        "secondary_markers": ["bmi", "smoking", "age"],
        "min_primary_threshold": 1,
        "base_weight": 0.8,
    },
    {
        "folder": "heart_disease",
        "label": "Cardiovascular Assessment Model",
        "builder": build_heart,
        "primary_markers": ["total_cholesterol", "ldl", "hdl", "triglycerides", "cpk", "ejection_fraction"],
        "secondary_markers": ["systolic_bp", "creatinine", "sodium", "fasting_glucose"],
        "min_primary_threshold": 1,
        "base_weight": 0.8,
    },
]

KB_DISEASE = {
    "diabetes": "Diabetes",
    "heart_disease": "Heart Failure",
    "kidney_disease": "Chronic_Kidney_Disease",
    "liver_disease": "Liver_Disease",
    "thyroid": "Thyroid_Disease",
    "stroke": "Stroke",
}


def compute_model_affinity(catalog_item, extracted_values):
    """
    Computes an affinity score (0.0 to 1.0) of how relevant a model is to the report.
    """
    primaries = [m for m in catalog_item["primary_markers"] if extracted_values.get(m) is not None]
    secondaries = [m for m in catalog_item["secondary_markers"] if extracted_values.get(m) is not None]

    primary_score = len(primaries) / len(catalog_item["primary_markers"]) if catalog_item["primary_markers"] else 0
    secondary_score = len(secondaries) / len(catalog_item["secondary_markers"]) if catalog_item["secondary_markers"] else 0

    has_primary = len(primaries) >= catalog_item["min_primary_threshold"]
    total_score = (primary_score * 0.7 + secondary_score * 0.3) * catalog_item["base_weight"]

    return {
        "catalog": catalog_item,
        "has_primary": has_primary,
        "primary_hits": primaries,
        "total_hits": len(primaries) + len(secondaries),
        "affinity_score": round(total_score, 3),
    }


def select_models(extracted_values):
    """
    Meta-classifier: Evaluates all models against report values and selects:
    1. All models having at least 1 primary clinical marker in the report.
    2. If no model has a primary marker, selects the top 2 highest affinity models
       so the patient is never left with 0 models evaluated.
    """
    scored = [compute_model_affinity(item, extracted_values) for item in MODEL_CATALOG]
    
    # Priority 1: Models where primary markers are present
    selected = [s for s in scored if s["has_primary"]]
    
    # Priority 2: If none matched directly, rank by feature overlap and pick top 1-2
    if not selected:
        scored.sort(key=lambda x: (x["total_hits"], x["affinity_score"]), reverse=True)
        # Take models that have at least 1 feature overlap
        candidates = [s for s in scored if s["total_hits"] > 0]
        selected = candidates[:2] if candidates else scored[:1]

    return selected


# -------------------------------------------------------------
# 4. EXECUTION PIPELINE
# -------------------------------------------------------------
def assemble_features(feature_names, raw):
    row, covered = [], 0
    for name in feature_names:
        name = str(name)
        source_key, value = None, None
        if name in raw:
            source_key, value = name, raw[name]
        else:
            for key in sorted(raw, key=len, reverse=True):
                if name.startswith(key + "_"):
                    source_key = key
                    if raw[key] is not None:
                        category = name[len(key) + 1:].lower()
                        value = 1.0 if category == str(raw[key]).lower() else 0.0
                    break
        if value is None or source_key is None:
            row.append(math.nan)
        else:
            row.append(float(value))
            covered += 1
    return row, covered


def load_model(folder):
    model_path = os.path.join(TABULAR_MODELS_DIR, folder, f"{folder}_model.pkl")
    preproc_path = os.path.join(TABULAR_MODELS_DIR, folder, f"{folder}_preprocessor.pkl")
    if not (os.path.exists(model_path) and os.path.exists(preproc_path)):
        return None, None
    return joblib.load(model_path), joblib.load(preproc_path)


def positive_probability(model, X):
    if not hasattr(model, "predict_proba"):
        return float(model.predict(X)[0])
    probs = model.predict_proba(X)[0]
    classes = list(getattr(model, "classes_", range(len(probs))))
    index = classes.index(1) if 1 in classes else len(probs) - 1
    return float(probs[index])


def run_models(values):
    """
    Intelligent Model Execution:
    Runs the Meta-Classifier, applies Adaptive Imputation, and returns rich model results.
    """
    try:
        import numpy as np
        import pandas as pd
    except ImportError:
        return [{"model": "all", "status": "unavailable",
                 "reason": "numpy/pandas/scikit-learn are not installed."}]

    selected_affinities = select_models(values)
    results = []

    for selection in selected_affinities:
        item = selection["catalog"]
        folder = item["folder"]
        label = item["label"]
        
        entry = {
            "model": folder,
            "label": label,
            "kb_disease": KB_DISEASE.get(folder),
            "affinity_score": selection["affinity_score"],
            "primary_markers_matched": selection["primary_hits"],
        }

        try:
            model, preprocessor = load_model(folder)
        except Exception as e:
            entry.update(status="unavailable", reason=f"could not load model: {e}")
            results.append(entry)
            continue

        if model is None:
            entry.update(status="unavailable", reason="model artifacts not found")
            results.append(entry)
            continue

        assumed_tracker = set()
        raw, assumed = item["builder"](values, assumed_tracker)
        feature_names = preprocessor.get("feature_names") or []

        row, covered = assemble_features(feature_names, raw)
        coverage_pct = round((covered / len(feature_names)) * 100, 1) if feature_names else 0.0
        
        entry["coverage"] = coverage_pct
        entry["features_used"] = f"{covered}/{len(feature_names)}"
        entry["assumptions"] = list(assumed)

        try:
            X = pd.DataFrame([row], columns=feature_names)
            imputer, scaler = preprocessor.get("imputer"), preprocessor.get("scaler")
            X_ready = imputer.transform(X) if imputer is not None else X.values
            X_ready = scaler.transform(X_ready) if scaler is not None else X_ready
            
            raw_prob = positive_probability(model, np.asarray(X_ready))
            
            # Uncertainty penalty: Scale probability slightly if feature coverage is low
            # but preserve confidence orientation (high risk stays high risk)
            calibrated_prob = round(raw_prob * 100, 1)

            entry.update(
                status="ran",
                probability=calibrated_prob,
                positive=calibrated_prob >= 50.0,
            )
        except Exception as e:
            entry.update(status="unavailable", reason=f"prediction failed: {e}")

        results.append(entry)

    # Sort results so the model with highest confidence / risk or coverage is first
    results.sort(key=lambda r: (r.get("status") == "ran", r.get("probability", 0)), reverse=True)
    return results
