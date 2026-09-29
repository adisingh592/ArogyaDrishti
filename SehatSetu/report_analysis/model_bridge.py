"""
SehatSetu - Report-to-Model Bridge
Maps values parsed from a medical report onto the input features of the trained
tabular models (SehatSetu/models/tabular/) and runs them.

A model only runs when the report contains its key inputs and enough of its features.
Missing features are filled by the model's own median imputer, so predictions made
from a small subset of features are reported together with their feature coverage.
"""

import math
import os

SEHATSETU_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABULAR_MODELS_DIR = os.path.join(SEHATSETU_DIR, "models", "tabular")


# -------------------------------------------------------------
# 1. HELPERS TO DERIVE MODEL INPUTS FROM REPORT VALUES
# -------------------------------------------------------------
def flag(v, key, derived=None):
    """
    Combines a Yes/No history answer in the report with a lab-based rule: True if either says
    True (a measured high BP counts even when the history says 'No'), else False/None.
    """
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
        return v["systolic_bp"] >= 130 or v["diastolic_bp"] >= 80
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
    """BRFSS 13-level age category: 1 = 18-24, 2 = 25-29, ... 12 = 75-79, 13 = 80+."""
    if age is None:
        return None
    if age < 25:
        return 1
    return min(13, int((age - 25) // 5) + 2)


def sex01(v):
    return None if "sex" not in v else (1 if v["sex"] == "male" else 0)


# -------------------------------------------------------------
# 2. PER-MODEL INPUT BUILDERS
# Each returns (raw_record, assumed_keys). raw values of None mean "not in the report".
# assumed_keys are filled with a safe default but do not count as report coverage.
# -------------------------------------------------------------
def build_diabetes(v):
    smoker = flag(v, "smoking")
    raw = {
        "HighBP": as01(flag(v, "hypertension", has_hypertension(v))),
        "HighChol": as01(v["total_cholesterol"] >= 240) if "total_cholesterol" in v else None,
        "CholCheck": 1 if "total_cholesterol" in v else None,
        "BMI": v.get("bmi"),
        "Smoker": as01(smoker),
        "Stroke": as01(flag(v, "stroke_history")),
        "HeartDiseaseorAttack": as01(flag(v, "heart_disease")),
        "Sex": sex01(v),
        "Age": brfss_age_group(v.get("age")),
    }
    return raw, set()


def build_heart(v):
    raw = {
        # Heart failure clinical records features
        "age": v.get("age"),
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
        # UCI Cleveland features (used if the model was trained on that dataset instead)
        "trestbps": v.get("systolic_bp"),
        "chol": v.get("total_cholesterol"),
        "fbs": as01(v["fasting_glucose"] > 120) if "fasting_glucose" in v else None,
    }
    return raw, set()


def build_kidney(v):
    raw = {
        "age": v.get("age"),
        "bp": v.get("diastolic_bp"),          # CKD dataset records diastolic pressure
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
    return raw, set()


def build_liver(v):
    raw = {
        "Age": v.get("age"),
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
    return raw, set()


def build_thyroid(v):
    # Column layout of UCI hypothyroid.data (0 = target). Lab units: TSH mIU/L, T3 nmol/L, TT4 nmol/L.
    def measured(key):
        return "y" if v.get(key) is not None else "n"

    # FTI (free thyroxine index) = TT4 / T4U is the model's strongest feature but is rarely on
    # modern reports. Estimate it from total T4 with the dataset's median T4U (0.96), because
    # the imputer would otherwise fill a normal FTI and mask a high TSH.
    tt4_nmol = v["t4"] * 12.87 if v.get("t4") is not None else None
    fti = round(tt4_nmol / 0.96, 1) if tt4_nmol is not None else None

    raw = {
        "feature_1": v.get("age"),
        "feature_2": None if "sex" not in v else ("M" if v["sex"] == "male" else "F"),
        "feature_14": measured("tsh"),
        "feature_15": v.get("tsh"),
        "feature_16": measured("t3"),
        "feature_17": v["t3"] * 0.01536 if v.get("t3") is not None else None,
        "feature_18": measured("t4"),
        "feature_19": tt4_nmol,
        "feature_20": "n", "feature_21": None,     # T4U
        "feature_22": measured("t4"), "feature_23": fti,   # FTI (estimated)
        "feature_24": "n", "feature_25": None,     # TBG
    }
    # History flags (on thyroxine, surgery, pregnant, ...) default to "f" = not reported
    assumed = set()
    for col in range(3, 14):
        raw[f"feature_{col}"] = "f"
        assumed.add(f"feature_{col}")
    assumed.update({"feature_20", "feature_22", "feature_24"})
    return raw, assumed


def build_stroke(v):
    smoking = v.get("smoking")
    raw = {
        "gender": None if "sex" not in v else v["sex"].capitalize(),
        "age": v.get("age"),
        "hypertension": as01(flag(v, "hypertension", has_hypertension(v))),
        "heart_disease": as01(flag(v, "heart_disease")),
        "ever_married": None,
        "work_type": None,
        "Residence_type": None,
        "avg_glucose_level": any_glucose(v),
        "bmi": v.get("bmi"),
        "smoking_status": None if smoking is None else
            ("formerly smoked" if smoking == "former" else "smokes" if smoking else "never smoked"),
    }
    return raw, set()


# folder name, display label, builder, required report keys, minimum feature coverage
MODEL_CONFIGS = [
    ("diabetes", "Diabetes risk (BRFSS survey model)", build_diabetes, ["bmi", "age"], 0.5),
    ("heart_disease", None, build_heart, ["age"], 0.5),
    ("kidney_disease", "Chronic kidney disease", build_kidney, ["creatinine"], 0.4),
    ("liver_disease", "Liver disease (ILPD model)", build_liver, ["alt", "ast"], 0.6),
    ("thyroid", "Hypothyroidism", build_thyroid, ["tsh"], 0.3),
    ("stroke", "Stroke risk", build_stroke, ["age"], 0.5),
]

KB_DISEASE = {
    "diabetes": "Diabetes", "heart_disease": "Heart Failure", "kidney_disease": "Chronic_Kidney_Disease",
    "liver_disease": "Liver_Disease", "thyroid": "Thyroid_Disease", "stroke": "Stroke",
}


# -------------------------------------------------------------
# 3. FEATURE ASSEMBLY AND PREDICTION
# -------------------------------------------------------------
def assemble_features(feature_names, raw, assumed):
    """
    Builds one row in the model's feature order. Handles one-hot columns created with
    pd.get_dummies (e.g. 'gender_Male', 'htn_yes'). Returns (row, covered_count).
    """
    row, covered = [], 0
    for name in feature_names:
        name = str(name)
        source_key, value = None, None
        if name in raw:
            source_key, value = name, raw[name]
        else:
            # longest matching prefix wins, so 'feature_14_y' maps to 'feature_14', not 'feature_1'
            for key in sorted(raw, key=len, reverse=True):
                if name.startswith(key + "_"):
                    source_key = key
                    if raw[key] is not None:
                        # exact match: raw datasets contain dirty duplicates like 'dm_ yes' next to 'dm_yes'
                        category = name[len(key) + 1:].lower()
                        value = 1.0 if category == str(raw[key]).lower() else 0.0
                    break
        if value is None or source_key is None:
            row.append(math.nan)
        else:
            row.append(float(value))
            if source_key not in assumed:
                covered += 1
    return row, covered


def load_model(folder):
    import joblib
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
    Returns a list of dicts, one per model: status 'ran' with probability, or
    'skipped' / 'unavailable' with the reason.
    """
    try:
        import numpy as np
        import pandas as pd
    except ImportError:
        return [{"model": "all", "status": "unavailable",
                 "reason": "numpy/pandas/scikit-learn are not installed (pip install -r requirements.txt)."}]

    results = []
    for folder, label, builder, required, min_coverage in MODEL_CONFIGS:
        entry = {"model": folder, "label": label or folder.replace("_", " ").title(),
                 "kb_disease": KB_DISEASE.get(folder)}

        missing = [key for key in required if values.get(key) is None]
        if missing:
            entry.update(status="skipped", reason=f"report is missing: {', '.join(missing)}")
            results.append(entry)
            continue

        try:
            model, preprocessor = load_model(folder)
        except Exception as e:
            entry.update(status="unavailable", reason=f"could not load model ({e})")
            results.append(entry)
            continue
        if model is None:
            entry.update(status="unavailable", reason="model not trained yet (run its train.py)")
            results.append(entry)
            continue

        feature_names = preprocessor.get("feature_names") or []
        if folder == "heart_disease":
            target = preprocessor.get("target_col")
            if target == "DEATH_EVENT":
                entry["label"] = "Heart failure mortality risk"
                if values.get("ejection_fraction") is None:
                    entry.update(status="skipped", reason="report is missing: ejection_fraction")
                    results.append(entry)
                    continue
            else:
                entry["label"] = "Heart disease"

        raw, assumed = builder(values)
        row, covered = assemble_features(feature_names, raw, assumed)
        coverage = covered / len(feature_names) if feature_names else 0.0
        entry["coverage"] = round(coverage * 100, 1)
        entry["features_used"] = f"{covered}/{len(feature_names)}"

        if coverage < min_coverage:
            entry.update(status="skipped",
                         reason=f"only {covered} of {len(feature_names)} model inputs are in the report "
                                f"(needs {int(min_coverage * 100)}%)")
            results.append(entry)
            continue

        try:
            X = pd.DataFrame([row], columns=feature_names)
            imputer, scaler = preprocessor.get("imputer"), preprocessor.get("scaler")
            X_ready = imputer.transform(X) if imputer is not None else X.values
            X_ready = scaler.transform(X_ready) if scaler is not None else X_ready
            prob = positive_probability(model, np.asarray(X_ready))
        except Exception as e:
            entry.update(status="unavailable", reason=f"prediction failed ({e})")
            results.append(entry)
            continue

        entry.update(status="ran", probability=round(prob * 100, 1), positive=prob >= 0.5)
        results.append(entry)
    return results
