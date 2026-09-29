"""
SehatSetu - Clinical Rule Engine
Checks report values against published adult reference ranges and diagnostic cut-offs.

Every rule is deterministic and cites where its threshold comes from. Reference ranges
differ slightly between laboratories, so results are screening flags, not a diagnosis.
"""

# Severity levels used everywhere in the report analysis
NORMAL, BORDERLINE, ABNORMAL, URGENT = 0, 1, 2, 3
SEVERITY_LABELS = {NORMAL: "Normal", BORDERLINE: "Borderline", ABNORMAL: "Abnormal", URGENT: "Urgent"}


def finding(condition, parameter, value, unit, severity, message, reference, kb_disease=None):
    return {
        "condition": condition,
        "parameter": parameter,
        "value": value,
        "unit": unit,
        "severity": severity,
        "status": SEVERITY_LABELS[severity],
        "message": message,
        "reference": reference,
        "kb_disease": kb_disease,   # key in recommendation/disease_information.json
    }


def is_female(v):
    return v.get("sex") == "female"


# -------------------------------------------------------------
# DIABETES (American Diabetes Association, Standards of Care)
# -------------------------------------------------------------
def check_diabetes(v):
    out = []
    ref = "ADA Standards of Care: HbA1c >=6.5% / FPG >=126 / 2-h PG >=200 / random PG >=200 mg/dL = diabetes"
    c, kb = "Diabetes", "Diabetes"

    if "hba1c" in v:
        x = v["hba1c"]
        if x >= 6.5:
            out.append(finding(c, "HbA1c", x, "%", ABNORMAL, "In the diabetes range (>= 6.5%).", ref, kb))
        elif x >= 5.7:
            out.append(finding(c, "HbA1c", x, "%", BORDERLINE, "Prediabetes range (5.7-6.4%).", ref, kb))
        else:
            out.append(finding(c, "HbA1c", x, "%", NORMAL, "Normal (< 5.7%).", ref))

    if "fasting_glucose" in v:
        x = v["fasting_glucose"]
        if x < 54:
            out.append(finding(c, "Fasting Glucose", x, "mg/dL", URGENT, "Very low blood sugar (< 54 mg/dL, level 2 hypoglycaemia).", ref, kb))
        elif x >= 126:
            out.append(finding(c, "Fasting Glucose", x, "mg/dL", ABNORMAL, "In the diabetes range (>= 126 mg/dL).", ref, kb))
        elif x >= 100:
            out.append(finding(c, "Fasting Glucose", x, "mg/dL", BORDERLINE, "Impaired fasting glucose / prediabetes (100-125 mg/dL).", ref, kb))
        elif x < 70:
            out.append(finding(c, "Fasting Glucose", x, "mg/dL", BORDERLINE, "Below normal (< 70 mg/dL).", ref, kb))
        else:
            out.append(finding(c, "Fasting Glucose", x, "mg/dL", NORMAL, "Normal (70-99 mg/dL).", ref))

    if "pp_glucose" in v:
        x = v["pp_glucose"]
        if x >= 200:
            out.append(finding(c, "Post-Prandial Glucose", x, "mg/dL", ABNORMAL, "In the diabetes range (>= 200 mg/dL).", ref, kb))
        elif x >= 140:
            out.append(finding(c, "Post-Prandial Glucose", x, "mg/dL", BORDERLINE, "Impaired glucose tolerance (140-199 mg/dL).", ref, kb))
        else:
            out.append(finding(c, "Post-Prandial Glucose", x, "mg/dL", NORMAL, "Normal (< 140 mg/dL).", ref))

    if "random_glucose" in v:
        x = v["random_glucose"]
        if x >= 400:
            out.append(finding(c, "Random Glucose", x, "mg/dL", URGENT, "Very high blood sugar (>= 400 mg/dL).", ref, kb))
        elif x >= 200:
            out.append(finding(c, "Random Glucose", x, "mg/dL", ABNORMAL, "In the diabetes range (>= 200 mg/dL) - confirm with fasting glucose or HbA1c.", ref, kb))
        elif x < 54:
            out.append(finding(c, "Random Glucose", x, "mg/dL", URGENT, "Very low blood sugar (< 54 mg/dL).", ref, kb))
        else:
            out.append(finding(c, "Random Glucose", x, "mg/dL", NORMAL, "Below the diabetes cut-off (< 200 mg/dL).", ref))

    if v.get("urine_sugar", 0) >= 1:
        out.append(finding(c, "Urine Sugar", v["urine_sugar"], "grade", BORDERLINE, "Sugar present in urine - check blood glucose.", ref, kb))
    return out


# -------------------------------------------------------------
# BLOOD PRESSURE (2017 ACC/AHA guideline) and LIPIDS (NCEP ATP III)
# -------------------------------------------------------------
def check_blood_pressure(v):
    if "systolic_bp" not in v or "diastolic_bp" not in v:
        return []
    s, d = v["systolic_bp"], v["diastolic_bp"]
    ref = "2017 ACC/AHA: <120/<80 normal, 120-129/<80 elevated, 130-139 or 80-89 stage 1, >=140 or >=90 stage 2, >180 and/or >120 crisis"
    c, kb, val = "Hypertension", "Heart Disease", f"{s:.0f}/{d:.0f}"

    if s > 180 or d > 120:
        return [finding(c, "Blood Pressure", val, "mmHg", URGENT, "Hypertensive crisis range (> 180/120).", ref, kb)]
    if s >= 140 or d >= 90:
        return [finding(c, "Blood Pressure", val, "mmHg", ABNORMAL, "Stage 2 hypertension (>= 140/90).", ref, kb)]
    if s >= 130 or d >= 80:
        return [finding(c, "Blood Pressure", val, "mmHg", ABNORMAL, "Stage 1 hypertension (130-139 / 80-89).", ref, kb)]
    if s >= 120:
        return [finding(c, "Blood Pressure", val, "mmHg", BORDERLINE, "Elevated blood pressure (120-129 / < 80).", ref, kb)]
    if s < 90 or d < 60:
        return [finding(c, "Blood Pressure", val, "mmHg", BORDERLINE, "Low blood pressure (< 90/60).", ref)]
    return [finding(c, "Blood Pressure", val, "mmHg", NORMAL, "Normal (< 120/80).", ref)]


def check_lipids(v):
    out = []
    ref = "NCEP ATP III lipid classification"
    c, kb = "Cholesterol / Cardiovascular Risk", "Heart Disease"

    if "total_cholesterol" in v:
        x = v["total_cholesterol"]
        sev, msg = (ABNORMAL, "High (>= 240 mg/dL).") if x >= 240 else \
                   (BORDERLINE, "Borderline high (200-239 mg/dL).") if x >= 200 else (NORMAL, "Desirable (< 200 mg/dL).")
        out.append(finding(c, "Total Cholesterol", x, "mg/dL", sev, msg, ref, kb if sev else None))
    if "ldl" in v:
        x = v["ldl"]
        sev, msg = (ABNORMAL, "Very high (>= 190 mg/dL).") if x >= 190 else \
                   (ABNORMAL, "High (160-189 mg/dL).") if x >= 160 else \
                   (BORDERLINE, "Borderline high (130-159 mg/dL).") if x >= 130 else (NORMAL, "Acceptable (< 130 mg/dL).")
        out.append(finding(c, "LDL Cholesterol", x, "mg/dL", sev, msg, ref, kb if sev else None))
    if "hdl" in v:
        x, low = v["hdl"], 50 if is_female(v) else 40
        if x < low:
            out.append(finding(c, "HDL Cholesterol", x, "mg/dL", BORDERLINE, f"Low (< {low} mg/dL) - raises heart risk.", ref, kb))
        else:
            out.append(finding(c, "HDL Cholesterol", x, "mg/dL", NORMAL, f"Acceptable (>= {low} mg/dL).", ref))
    if "triglycerides" in v:
        x = v["triglycerides"]
        sev, msg = (URGENT, "Very high (>= 1000 mg/dL) - risk of pancreatitis.") if x >= 1000 else \
                   (ABNORMAL, "High (>= 200 mg/dL).") if x >= 200 else \
                   (BORDERLINE, "Borderline high (150-199 mg/dL).") if x >= 150 else (NORMAL, "Normal (< 150 mg/dL).")
        out.append(finding(c, "Triglycerides", x, "mg/dL", sev, msg, ref, kb if sev else None))
    return out


def check_heart_function(v):
    if "ejection_fraction" not in v:
        return []
    x = v["ejection_fraction"]
    ref = "2022 AHA/ACC/HFSA heart failure guideline: EF <=40% reduced, 41-49% mildly reduced, >=50% preserved"
    c, kb = "Heart Failure", "Heart Failure"
    if x <= 40:
        return [finding(c, "Ejection Fraction", x, "%", ABNORMAL, "Reduced ejection fraction (<= 40%).", ref, kb)]
    if x < 50:
        return [finding(c, "Ejection Fraction", x, "%", BORDERLINE, "Mildly reduced ejection fraction (41-49%).", ref, kb)]
    return [finding(c, "Ejection Fraction", x, "%", NORMAL, "Normal (>= 50%).", ref)]


# -------------------------------------------------------------
# ANAEMIA and BLOOD COUNTS (WHO haemoglobin thresholds)
# -------------------------------------------------------------
def check_blood_count(v):
    out = []
    if "hemoglobin" in v:
        x = v["hemoglobin"]
        low = 12.0 if is_female(v) else 13.0
        ref = "WHO: anaemia if Hb < 13 g/dL (men) / < 12 g/dL (non-pregnant women); severe < 8 g/dL"
        c, kb = "Anaemia", "Anemia"
        if x < 7:
            out.append(finding(c, "Haemoglobin", x, "g/dL", URGENT, "Very low haemoglobin (< 7 g/dL).", ref, kb))
        elif x < 8:
            out.append(finding(c, "Haemoglobin", x, "g/dL", ABNORMAL, "Severe anaemia (< 8 g/dL).", ref, kb))
        elif x < 11:
            out.append(finding(c, "Haemoglobin", x, "g/dL", ABNORMAL, "Moderate anaemia (8-10.9 g/dL).", ref, kb))
        elif x < low:
            out.append(finding(c, "Haemoglobin", x, "g/dL", BORDERLINE, f"Mild anaemia (below {low} g/dL).", ref, kb))
        elif x > 18.5:
            out.append(finding("Blood Count", "Haemoglobin", x, "g/dL", ABNORMAL, "High haemoglobin (possible polycythaemia).", ref))
        else:
            out.append(finding(c, "Haemoglobin", x, "g/dL", NORMAL, f"Normal (>= {low} g/dL).", ref))

    c, ref = "Blood Count", "Typical adult reference: WBC 4,000-11,000 /uL; platelets 150,000-450,000 /uL"
    if "wbc" in v:
        x = v["wbc"]
        if x > 30000 or x < 2000:
            out.append(finding(c, "WBC Count", x, "/uL", URGENT, "Markedly abnormal white cell count - needs prompt review (infection or blood disorder).", ref))
        elif x > 11000:
            out.append(finding(c, "WBC Count", x, "/uL", ABNORMAL, "High white cell count (leukocytosis) - often infection or inflammation.", ref))
        elif x < 4000:
            out.append(finding(c, "WBC Count", x, "/uL", ABNORMAL, "Low white cell count (leukopenia).", ref))
        else:
            out.append(finding(c, "WBC Count", x, "/uL", NORMAL, "Normal.", ref))
    if "platelets" in v:
        x = v["platelets"]
        if x < 50000:
            out.append(finding(c, "Platelet Count", x, "/uL", URGENT, "Very low platelets (< 50,000) - bleeding risk.", ref))
        elif x < 150000:
            out.append(finding(c, "Platelet Count", x, "/uL", ABNORMAL, "Low platelets (thrombocytopenia).", ref))
        elif x > 450000:
            out.append(finding(c, "Platelet Count", x, "/uL", ABNORMAL, "High platelets (thrombocytosis).", ref))
        else:
            out.append(finding(c, "Platelet Count", x, "/uL", NORMAL, "Normal.", ref))
    return out


# -------------------------------------------------------------
# KIDNEY (KDIGO 2012 CKD staging, CKD-EPI 2021 eGFR equation)
# -------------------------------------------------------------
def egfr_ckd_epi_2021(creatinine, age, female):
    kappa, alpha = (0.7, -0.241) if female else (0.9, -0.302)
    ratio = creatinine / kappa
    egfr = 142 * min(ratio, 1) ** alpha * max(ratio, 1) ** -1.200 * 0.9938 ** age
    return egfr * 1.012 if female else egfr


def check_kidney(v):
    out = []
    ref = "KDIGO 2012: eGFR (CKD-EPI 2021) >=90 G1, 60-89 G2, 45-59 G3a, 30-44 G3b, 15-29 G4, <15 G5; CKD needs 3 months of abnormal results"
    c, kb = "Chronic Kidney Disease", "Chronic_Kidney_Disease"

    if "creatinine" in v and "age" in v and "sex" in v:
        egfr = round(egfr_ckd_epi_2021(v["creatinine"], v["age"], is_female(v)), 1)
        v["egfr"] = egfr
        if egfr < 15:
            out.append(finding(c, "eGFR", egfr, "mL/min/1.73m2", URGENT, "Kidney failure range (G5, < 15).", ref, kb))
        elif egfr < 30:
            out.append(finding(c, "eGFR", egfr, "mL/min/1.73m2", ABNORMAL, "Severely reduced kidney function (G4, 15-29).", ref, kb))
        elif egfr < 60:
            out.append(finding(c, "eGFR", egfr, "mL/min/1.73m2", ABNORMAL, "Moderately reduced kidney function (G3, 30-59).", ref, kb))
        elif egfr < 90:
            out.append(finding(c, "eGFR", egfr, "mL/min/1.73m2", BORDERLINE if egfr < 75 else NORMAL,
                               "Mildly reduced (G2, 60-89) - significant only with other kidney damage markers.", ref, kb if egfr < 75 else None))
        else:
            out.append(finding(c, "eGFR", egfr, "mL/min/1.73m2", NORMAL, "Normal (G1, >= 90).", ref))
    elif "creatinine" in v:
        x, high = v["creatinine"], 1.1 if is_female(v) else 1.3
        if x > high:
            out.append(finding(c, "Serum Creatinine", x, "mg/dL", ABNORMAL, f"Above the usual upper limit ({high} mg/dL). Add age and sex to compute eGFR.", ref, kb))
        else:
            out.append(finding(c, "Serum Creatinine", x, "mg/dL", NORMAL, "Within the usual range.", ref))

    if "urea" in v:
        x = v["urea"]
        if x > 100:
            out.append(finding(c, "Blood Urea", x, "mg/dL", ABNORMAL, "Markedly raised urea (> 100 mg/dL).", ref, kb))
        elif x > 45:
            out.append(finding(c, "Blood Urea", x, "mg/dL", BORDERLINE, "Raised urea (> 45 mg/dL) - can also be due to dehydration.", ref, kb))
        else:
            out.append(finding(c, "Blood Urea", x, "mg/dL", NORMAL, "Normal (15-45 mg/dL).", ref))

    if v.get("urine_albumin", 0) >= 1:
        sev = ABNORMAL if v["urine_albumin"] >= 2 else BORDERLINE
        out.append(finding(c, "Urine Albumin", v["urine_albumin"], "grade", sev, "Protein in urine (proteinuria) - a kidney damage marker.", ref, kb))

    c, ref = "Electrolytes", "Typical adult reference: sodium 135-145 mmol/L, potassium 3.5-5.0 mmol/L"
    if "potassium" in v:
        x = v["potassium"]
        if x >= 6.0 or x < 3.0:
            out.append(finding(c, "Potassium", x, "mmol/L", URGENT, "Dangerous potassium level - can affect heart rhythm.", ref))
        elif x > 5.0 or x < 3.5:
            out.append(finding(c, "Potassium", x, "mmol/L", ABNORMAL, "Potassium outside 3.5-5.0 mmol/L.", ref))
        else:
            out.append(finding(c, "Potassium", x, "mmol/L", NORMAL, "Normal.", ref))
    if "sodium" in v:
        x = v["sodium"]
        if x < 125 or x > 155:
            out.append(finding(c, "Sodium", x, "mmol/L", URGENT, "Severely abnormal sodium.", ref))
        elif x < 135 or x > 145:
            out.append(finding(c, "Sodium", x, "mmol/L", ABNORMAL, "Sodium outside 135-145 mmol/L.", ref))
        else:
            out.append(finding(c, "Sodium", x, "mmol/L", NORMAL, "Normal.", ref))
    return out


# -------------------------------------------------------------
# LIVER (typical adult reference intervals; ACG guidance on abnormal liver chemistry)
# -------------------------------------------------------------
def check_liver(v):
    out = []
    ref = "Typical adult reference: ALT/AST <= 40 U/L, ALP 44-147 U/L, total bilirubin <= 1.2 mg/dL, albumin 3.5-5.0 g/dL"
    c, kb = "Liver Disease", "Liver_Disease"

    for key, name in (("alt", "ALT (SGPT)"), ("ast", "AST (SGOT)")):
        if key in v:
            x = v[key]
            if x > 1000:
                out.append(finding(c, name, x, "U/L", URGENT, "Extremely high (> 25x normal) - possible acute liver injury.", ref, kb))
            elif x > 200:
                out.append(finding(c, name, x, "U/L", ABNORMAL, "Markedly raised (> 5x normal).", ref, kb))
            elif x > 40:
                out.append(finding(c, name, x, "U/L", BORDERLINE, "Mildly raised (> 40 U/L).", ref, kb))
            else:
                out.append(finding(c, name, x, "U/L", NORMAL, "Normal.", ref))
    if "alp" in v:
        x = v["alp"]
        if x > 147:
            out.append(finding(c, "Alkaline Phosphatase", x, "U/L", BORDERLINE if x < 300 else ABNORMAL, "Raised (> 147 U/L) - liver/bile duct or bone origin.", ref, kb))
        else:
            out.append(finding(c, "Alkaline Phosphatase", x, "U/L", NORMAL, "Normal.", ref))
    if "total_bilirubin" in v:
        x = v["total_bilirubin"]
        if x > 3:
            out.append(finding(c, "Total Bilirubin", x, "mg/dL", ABNORMAL, "High bilirubin (> 3 mg/dL) - visible jaundice likely.", ref, kb))
        elif x > 1.2:
            out.append(finding(c, "Total Bilirubin", x, "mg/dL", BORDERLINE, "Mildly raised (> 1.2 mg/dL).", ref, kb))
        else:
            out.append(finding(c, "Total Bilirubin", x, "mg/dL", NORMAL, "Normal.", ref))
    if "albumin" in v:
        x = v["albumin"]
        if x < 3.5:
            out.append(finding(c, "Serum Albumin", x, "g/dL", BORDERLINE if x >= 3.0 else ABNORMAL, "Low albumin (< 3.5 g/dL) - liver, kidney or nutrition cause.", ref, kb))
        else:
            out.append(finding(c, "Serum Albumin", x, "g/dL", NORMAL, "Normal.", ref))
    return out


# -------------------------------------------------------------
# THYROID (American Thyroid Association)
# -------------------------------------------------------------
def check_thyroid(v):
    if "tsh" not in v:
        return []
    x = v["tsh"]
    ref = "ATA: typical TSH 0.4-4.5 mIU/L; high TSH with low free T4 = overt hypothyroidism, normal free T4 = subclinical"
    c, kb = "Thyroid Disease", "Thyroid_Disease"
    ft4_low = v.get("ft4") is not None and v["ft4"] < 0.8
    ft4_high = v.get("ft4") is not None and v["ft4"] > 1.8
    t4_low = v.get("t4") is not None and v["t4"] < 5.0
    t4_high = v.get("t4") is not None and v["t4"] > 12.0

    if x > 4.5:
        if x >= 10 or ft4_low or t4_low:
            return [finding(c, "TSH", x, "mIU/L", ABNORMAL, "Pattern of hypothyroidism (underactive thyroid).", ref, kb)]
        return [finding(c, "TSH", x, "mIU/L", BORDERLINE, "Mildly raised TSH (subclinical hypothyroidism) - repeat in 6-8 weeks.", ref, kb)]
    if x < 0.4:
        if x < 0.1 or ft4_high or t4_high:
            return [finding(c, "TSH", x, "mIU/L", ABNORMAL, "Pattern of hyperthyroidism (overactive thyroid).", ref, kb)]
        return [finding(c, "TSH", x, "mIU/L", BORDERLINE, "Low TSH (possible subclinical hyperthyroidism).", ref, kb)]
    return [finding(c, "TSH", x, "mIU/L", NORMAL, "Normal (0.4-4.5 mIU/L).", ref)]


# -------------------------------------------------------------
# BODY WEIGHT (WHO BMI classification)
# -------------------------------------------------------------
def check_bmi(v):
    if "bmi" not in v:
        return []
    x = v["bmi"]
    ref = "WHO BMI: < 18.5 underweight, 18.5-24.9 normal, 25-29.9 overweight, >= 30 obese (Asian populations: risk rises from 23)"
    c, kb = "Obesity / Weight", "Obesity"
    if x >= 35:
        return [finding(c, "BMI", x, "kg/m2", ABNORMAL, "Obesity class II or higher (>= 35).", ref, kb)]
    if x >= 30:
        return [finding(c, "BMI", x, "kg/m2", ABNORMAL, "Obesity (30-34.9).", ref, kb)]
    if x >= 25:
        return [finding(c, "BMI", x, "kg/m2", BORDERLINE, "Overweight (25-29.9).", ref, kb)]
    if x < 16:
        return [finding(c, "BMI", x, "kg/m2", ABNORMAL, "Severely underweight (< 16).", ref)]
    if x < 18.5:
        return [finding(c, "BMI", x, "kg/m2", BORDERLINE, "Underweight (< 18.5).", ref)]
    return [finding(c, "BMI", x, "kg/m2", NORMAL, "Normal (18.5-24.9).", ref)]


ALL_CHECKS = [check_diabetes, check_blood_pressure, check_lipids, check_heart_function,
              check_blood_count, check_kidney, check_liver, check_thyroid, check_bmi]


def run_clinical_rules(values):
    """Runs every rule on the parsed values and returns the list of findings."""
    v = dict(values)
    findings = []
    for check in ALL_CHECKS:
        findings.extend(check(v))
    if "egfr" in v:
        values["egfr"] = v["egfr"]
    return findings
