"""
SehatSetu - Medical Report Parser
Finds lab values (glucose, HbA1c, creatinine, TSH, haemoglobin, ...) in report text,
converts them to one standard unit, and rejects implausible readings.

Pure Python (standard library only) so it runs without the ML dependencies.
"""

import re

# -------------------------------------------------------------
# 1. PARAMETER DEFINITIONS
# -------------------------------------------------------------
# key: (display name, standard unit, alias regex, exclude regex or None)
# A line is used for a parameter when the alias matches and the exclude regex does not.
PARAMETERS = {
    "hba1c": ("HbA1c", "%", r"hb\s*a1c|\ba1c\b|glyc(?:at|osyl)ated\s*ha?emoglobin", None),
    "fasting_glucose": ("Fasting Blood Glucose", "mg/dL",
                        r"fasting\s*(?:blood|plasma)?\s*(?:sugar|glucose)|\bfbs\b|\bfbg\b|\bfpg\b|glucose[\s,\-]*\(?fasting",
                        None),
    "pp_glucose": ("Post-Prandial Glucose", "mg/dL",
                   r"post\s*-?\s*prandial\s*(?:blood|plasma)?\s*(?:sugar|glucose)|\bppbs\b|\bppbg\b|glucose[\s,\-]*\(?(?:pp|post)",
                   None),
    "random_glucose": ("Random Blood Glucose", "mg/dL",
                       r"random\s*(?:blood|plasma)?\s*(?:sugar|glucose)|\brbs\b|\brbg\b|^\s*(?:blood\s*|plasma\s*|serum\s*)?(?:sugar|glucose)\b",
                       r"fasting|prandial|\bpp\b|urine|\bfbs\b|\bppbs\b"),
    "hemoglobin": ("Haemoglobin", "g/dL", r"ha?emoglobin|\bhgb\b|\bhb\b",
                   r"a1c|glyc|corpuscular|\bmch|urine"),
    "total_cholesterol": ("Total Cholesterol", "mg/dL",
                          r"total\s*cholesterol|cholesterol[\s,\-]*total|serum\s*cholesterol|^\s*cholesterol\b",
                          r"hdl|ldl|ratio"),
    "hdl": ("HDL Cholesterol", "mg/dL", r"\bhdl\b", r"ratio|non[\s\-]*hdl"),
    "ldl": ("LDL Cholesterol", "mg/dL", r"\bldl\b", r"ratio"),
    "triglycerides": ("Triglycerides", "mg/dL", r"triglyceride|\btgl?\b", None),
    "creatinine": ("Serum Creatinine", "mg/dL", r"creatinine",
                   r"kinase|phospho|clearance|ratio|urine|\bacr\b|albumin"),
    "urea": ("Blood Urea", "mg/dL", r"blood\s*urea|serum\s*urea|^\s*urea\b", r"nitrogen|\bbun\b|ratio"),
    "bun": ("Blood Urea Nitrogen", "mg/dL", r"\bbun\b|urea\s*nitrogen", r"ratio"),
    "cpk": ("Creatine Phosphokinase", "U/L", r"creatin(?:in)?e\s*(?:phospho)?\s*kinase|\bcpk\b|\bck\b", r"mb\b|\bck-?mb"),
    "sodium": ("Sodium", "mmol/L", r"\bsodium\b|^\s*(?:serum\s*|s\.?\s*)?na\+?\b", None),
    "potassium": ("Potassium", "mmol/L", r"\bpotassium\b|^\s*(?:serum\s*|s\.?\s*)?k\+?\b", None),
    "total_bilirubin": ("Total Bilirubin", "mg/dL",
                        r"total\s*bilirubin|bilirubin[\s,\-]*\(?total|^\s*(?:serum\s*)?bilirubin\b",
                        r"direct|indirect|conjugated|urine"),
    "direct_bilirubin": ("Direct Bilirubin", "mg/dL",
                         r"direct\s*bilirubin|bilirubin[\s,\-]*\(?direct|conjugated\s*bilirubin",
                         r"indirect|unconjugated"),
    "alt": ("ALT (SGPT)", "U/L", r"\balt\b|\bsgpt\b|alanine\s*(?:amino)?\s*transferase|alanine\s*transaminase", None),
    "ast": ("AST (SGOT)", "U/L", r"\bast\b|\bsgot\b|aspartate\s*(?:amino)?\s*transferase|aspartate\s*transaminase", None),
    "alp": ("Alkaline Phosphatase", "U/L", r"alkaline\s*phosphatase|\balp\b|alk\.?\s*phos", None),
    "total_protein": ("Total Protein", "g/dL", r"total\s*proteins?|serum\s*proteins?|proteins?[\s,\-]*total", r"urine"),
    "albumin": ("Serum Albumin", "g/dL", r"^\s*(?:serum\s*)?albumin\b",
                r"urine|micro|globulin|a\s*/\s*g|ratio|creatinine"),
    "globulin": ("Globulin", "g/dL", r"^\s*(?:serum\s*)?globulin\b", r"ratio"),
    "ag_ratio": ("A/G Ratio", "", r"a\s*/\s*g\s*ratio|albumin\s*/?\s*globulin\s*ratio", None),
    "tsh": ("TSH", "mIU/L", r"\btsh\b|thyroid\s*stimulating\s*hormone", None),
    "t3": ("Total T3", "ng/dL", r"\bt3\b|triiodothyronine", r"free|\bft3\b|uptake"),
    "t4": ("Total T4", "ug/dL", r"\bt4\b|thyroxine", r"free|\bft4\b|uptake|\bt4u\b"),
    "ft4": ("Free T4", "ng/dL", r"free\s*t4|\bft4\b|free\s*thyroxine", None),
    "wbc": ("Total WBC Count", "cells/uL",
            r"\bwbc\b|\btlc\b|total\s*leu[ck]ocyte|white\s*blood\s*cell|\btc\b", r"morphology"),
    "rbc": ("RBC Count", "million/uL", r"\brbc\b|red\s*blood\s*cell", r"morphology|urine|\brbc\s*/\s*hpf"),
    "platelets": ("Platelet Count", "/uL", r"platelet|\bplt\b", r"volume|\bmpv\b|distribution"),
    "pcv": ("PCV / Haematocrit", "%", r"\bpcv\b|ha?ematocrit|\bhct\b|packed\s*cell\s*volume", None),
    "bmi": ("BMI", "kg/m2", r"\bbmi\b|body\s*mass\s*index", None),
    "height": ("Height", "cm", r"\bheight\b", None),
    "weight": ("Weight", "kg", r"\bweight\b", r"birth|molecular"),
    "ejection_fraction": ("Ejection Fraction", "%", r"ejection\s*fraction|\blvef\b|\bef\b", None),
    "specific_gravity": ("Urine Specific Gravity", "", r"specific\s*gravity|\bsp\.?\s*gr", None),
}

# Values outside these ranges (after unit conversion) are treated as misreads and dropped
PLAUSIBLE = {
    "hba1c": (3, 20), "fasting_glucose": (20, 1000), "pp_glucose": (20, 1000), "random_glucose": (20, 1000),
    "hemoglobin": (2, 25), "total_cholesterol": (50, 700), "hdl": (5, 200), "ldl": (10, 500),
    "triglycerides": (20, 5000), "creatinine": (0.1, 25), "urea": (2, 400), "bun": (1, 200),
    "cpk": (5, 50000), "sodium": (100, 180), "potassium": (1.5, 10), "total_bilirubin": (0.05, 50),
    "direct_bilirubin": (0.01, 30), "alt": (1, 10000), "ast": (1, 10000), "alp": (5, 5000),
    "total_protein": (2, 15), "albumin": (0.5, 7), "globulin": (0.5, 10), "ag_ratio": (0.1, 5),
    "tsh": (0.001, 500), "t3": (10, 1000), "t4": (0.5, 40), "ft4": (0.05, 10),
    "wbc": (100, 500000), "rbc": (0.5, 10), "platelets": (1000, 3000000), "pcv": (5, 75),
    "bmi": (10, 90), "height": (50, 250), "weight": (2, 400), "ejection_fraction": (5, 90),
    "specific_gravity": (1.000, 1.050), "age": (0, 120),
    "systolic_bp": (60, 300), "diastolic_bp": (30, 200),
}

# Yes/No history flags, e.g. "Smoker: Yes", "Hypertension: No"
FLAGS = {
    "smoking": r"smok(?:er|ing|es)?",
    "hypertension": r"hypertension|hypertensive|\bhtn\b",
    "diabetes_history": r"diabet(?:es|ic)\s*(?:history|mellitus)?|\bdm\b|\bt2dm\b",
    "heart_disease": r"heart\s*disease|coronary\s*artery\s*disease|\bcad\b|\bihd\b",
    "stroke_history": r"(?:history\s*of\s*)?stroke|\bcva\b",
    "pedal_edema": r"pedal\s*o?edema|leg\s*swelling",
    "poor_appetite": r"poor\s*appetite|loss\s*of\s*appetite|anorexia",
}
YES_WORDS = {"yes", "y", "positive", "present", "current", "true", "known", "smoker", "1"}
NO_WORDS = {"no", "n", "negative", "absent", "never", "false", "nil", "none", "0", "non-smoker", "nonsmoker"}

NUMBER_RE = re.compile(r"(?<![\w.])(\d{1,3}(?:,\d{2,3})+|\d+(?:\.\d+)?|\.\d+)")


# -------------------------------------------------------------
# 2. UNIT CONVERSION
# -------------------------------------------------------------
def convert_units(key, value, unit_text):
    u = unit_text.lower()

    if key in ("fasting_glucose", "pp_glucose", "random_glucose"):
        if "mmol" in u or value < 30:
            value *= 18.0
    elif key in ("total_cholesterol", "hdl", "ldl"):
        if "mmol" in u or value < 20:
            value *= 38.67
    elif key == "triglycerides":
        if "mmol" in u or value < 15:
            value *= 88.57
    elif key == "creatinine":
        if "mol" in u or value > 25:
            value /= 88.4
    elif key == "urea":
        if "mmol" in u:
            value *= 6.006
    elif key == "bun":
        if "mmol" in u:
            value *= 2.8
    elif key == "hemoglobin":
        if re.search(r"g\s*/\s*l\b", u) or value > 25:
            value /= 10.0
    elif key in ("albumin", "total_protein", "globulin"):
        if re.search(r"g\s*/\s*l\b", u) or value > 15:
            value /= 10.0
    elif key in ("total_bilirubin", "direct_bilirubin"):
        if "mol" in u:
            value /= 17.1
    elif key == "wbc":
        if value < 500:          # reported as x10^3/uL or x10^9/L
            value *= 1000
    elif key == "platelets":
        if "lakh" in u or "lac" in u:
            value *= 100000
        elif value < 2000:       # reported as x10^3/uL or x10^9/L
            value *= 1000
    elif key == "rbc":
        if value > 100:
            value /= 1e6
    elif key == "pcv":
        if value < 1:
            value *= 100
    elif key == "height":
        if "in" in u.split()[:1] or "inch" in u:
            value *= 2.54
        elif value < 3:          # metres
            value *= 100
    elif key == "weight":
        if "lb" in u:
            value *= 0.4536
    elif key == "t3":
        if re.search(r"ng\s*/\s*ml", u):
            value *= 100         # ng/mL -> ng/dL
        elif "nmol" in u or value < 10:
            value /= 0.01536     # nmol/L -> ng/dL
    elif key == "t4":
        if "nmol" in u or value > 40:
            value /= 12.87       # nmol/L -> ug/dL
    elif key == "ft4":
        if "pmol" in u or value > 10:
            value /= 12.87       # pmol/L -> ng/dL
    elif key == "specific_gravity":
        if value > 100:
            value /= 1000.0

    return value


def to_number(text):
    return float(text.replace(",", ""))


def is_plausible(key, value):
    low, high = PLAUSIBLE.get(key, (float("-inf"), float("inf")))
    return low <= value <= high


# -------------------------------------------------------------
# 3. EXTRACTION
# -------------------------------------------------------------
def extract_numeric(lines):
    values, sources = {}, {}

    for key, (_, _, alias, exclude) in PARAMETERS.items():
        alias_re = re.compile(alias, re.IGNORECASE)
        exclude_re = re.compile(exclude, re.IGNORECASE) if exclude else None

        for line in lines:
            match = alias_re.search(line)
            if not match or (exclude_re and exclude_re.search(line)):
                continue
            rest = line[match.end():]
            num = NUMBER_RE.search(rest)
            if not num:
                continue
            value = convert_units(key, to_number(num.group(1)), rest[num.end():num.end() + 25])
            if is_plausible(key, value):
                values[key] = round(value, 2)
                sources[key] = line.strip()
                break
    return values, sources


def extract_blood_pressure(lines):
    bp_re = re.compile(r"(?:blood\s*pressure|\bbp\b)[^0-9\n]{0,25}(\d{2,3})\s*/\s*(\d{2,3})", re.IGNORECASE)
    for line in lines:
        m = bp_re.search(line)
        if m:
            sys_bp, dia_bp = float(m.group(1)), float(m.group(2))
            if is_plausible("systolic_bp", sys_bp) and is_plausible("diastolic_bp", dia_bp):
                return {"systolic_bp": sys_bp, "diastolic_bp": dia_bp}, line.strip()
    return {}, None


def extract_age_sex(text):
    found = {}
    age = re.search(r"\bage\b[^0-9\n]{0,20}(\d{1,3})", text, re.IGNORECASE) or \
        re.search(r"\b(\d{1,3})\s*(?:yrs?|years?|y)\b(?:\s*(?:old|/))?", text, re.IGNORECASE)
    if age and is_plausible("age", float(age.group(1))):
        found["age"] = float(age.group(1))

    sex = re.search(r"\b(?:sex|gender)\b[^a-z\n]{0,20}\b(female|male|f|m)\b", text, re.IGNORECASE) or \
        re.search(r"\b\d{1,3}\s*(?:yrs?|years?|y)?\s*/\s*(female|male|f|m)\b", text, re.IGNORECASE) or \
        re.search(r"\b(female|male)\b", text, re.IGNORECASE)
    if sex:
        found["sex"] = "female" if sex.group(1).lower().startswith("f") else "male"
    return found


def extract_flags(lines):
    flags = {}
    answer_re = r"\s*[:\-=]?\s*\(?\s*(yes|no|y|n|positive|negative|present|absent|current|former|ex|never|nil|none|known|true|false|non-?smoker)\b"
    for key, alias in FLAGS.items():
        pattern = re.compile(r"(?:h/o\s*|history\s*of\s*)?(?:" + alias + r")" + answer_re, re.IGNORECASE)
        for line in lines:
            m = pattern.search(line)
            if not m:
                continue
            word = m.group(1).lower().replace("-", "")
            if word in ("former", "ex"):
                flags[key] = "former" if key == "smoking" else False
            elif word in YES_WORDS:
                flags[key] = True
            elif word in NO_WORDS:
                flags[key] = False
            if key in flags:
                break
    return flags


def extract_urine_grade(lines, alias):
    """Urine albumin / sugar are reported as Nil, Trace, 1+ .. 4+ (or +, ++, ...). Returns 0-5."""
    alias_re = re.compile(alias, re.IGNORECASE)
    for line in lines:
        m = alias_re.search(line)
        if not m:
            continue
        rest = line[m.end():].lower()
        if re.search(r"\b(nil|absent|negative|neg|not\s*detected)\b", rest):
            return 0.0
        if "trace" in rest:
            return 1.0
        plus = re.search(r"(\d)\s*\+|(\++)", rest)
        if plus:
            return float(plus.group(1)) if plus.group(1) else float(min(len(plus.group(2)), 5))
    return None


def parse_report(text):
    """
    Parses report text and returns:
      values  - {parameter_key: number or str/bool}
      sources - {parameter_key: the report line the value came from}
    """
    lines = [ln for ln in text.splitlines() if ln.strip()]

    values, sources = extract_numeric(lines)

    bp, bp_line = extract_blood_pressure(lines)
    values.update(bp)
    if bp_line:
        sources["systolic_bp"] = sources["diastolic_bp"] = bp_line

    values.update(extract_age_sex(text))
    values.update(extract_flags(lines))

    urine_albumin = extract_urine_grade(lines, r"urine\s*(?:albumin|protein)|albumin\s*\(urine\)|proteinuria")
    if urine_albumin is not None:
        values["urine_albumin"] = urine_albumin
    urine_sugar = extract_urine_grade(lines, r"urine\s*(?:sugar|glucose)|glycosuria")
    if urine_sugar is not None:
        values["urine_sugar"] = urine_sugar

    return add_derived_values(values), sources


def add_derived_values(values):
    """Fills in values that can be calculated from others (BMI, globulin, A/G ratio, urea/BUN)."""
    v = dict(values)
    if "bmi" not in v and "height" in v and "weight" in v:
        v["bmi"] = round(v["weight"] / (v["height"] / 100.0) ** 2, 1)
    if "globulin" not in v and "total_protein" in v and "albumin" in v:
        v["globulin"] = round(v["total_protein"] - v["albumin"], 2)
    if "ag_ratio" not in v and "albumin" in v and v.get("globulin"):
        v["ag_ratio"] = round(v["albumin"] / v["globulin"], 2)
    if "urea" not in v and "bun" in v:
        v["urea"] = round(v["bun"] * 2.14, 1)
    return v


def normalize_manual_values(raw):
    """Cleans a dict of values given directly (JSON file or --value key=val) into parser format."""
    values = {}
    for key, val in raw.items():
        k = key.strip().lower().replace(" ", "_")
        if k in ("gender",):
            k = "sex"
        if k == "sex":
            values[k] = "female" if str(val).lower().startswith("f") else "male"
        elif k == "bp" and isinstance(val, str) and "/" in val:
            s, d = val.split("/", 1)
            values["systolic_bp"], values["diastolic_bp"] = float(s), float(d)
        elif k in FLAGS:
            values[k] = str(val).strip().lower() in YES_WORDS
        else:
            try:
                values[k] = float(val)
            except (TypeError, ValueError):
                values[k] = val
    return add_derived_values(values)


OTHER_NAMES = {"systolic_bp": ("Systolic BP", "mmHg"), "diastolic_bp": ("Diastolic BP", "mmHg"),
               "age": ("Age", "years"), "sex": ("Sex", ""), "egfr": ("eGFR (CKD-EPI 2021)", "mL/min/1.73m2"),
               "urine_albumin": ("Urine Albumin (grade)", ""), "urine_sugar": ("Urine Sugar (grade)", "")}


def display_name(key):
    if key in PARAMETERS:
        return PARAMETERS[key][0]
    if key in OTHER_NAMES:
        return OTHER_NAMES[key][0]
    return key.replace("_", " ").title()


def unit_of(key):
    if key in PARAMETERS:
        return PARAMETERS[key][1]
    return OTHER_NAMES.get(key, ("", ""))[1]
