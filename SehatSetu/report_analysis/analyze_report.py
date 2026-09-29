"""
SehatSetu - Medical Report Analyzer

Reads a patient's medical/lab report, extracts the test values, examines them with
(1) clinical reference-range rules and (2) the trained ML models, and makes a
triage decision with health guidance from the recommendation system.

Usage:
    python analyze_report.py                              # interactive mode
    python analyze_report.py report.pdf                   # PDF / TXT / PNG / JPG / JSON report
    python analyze_report.py --text "HbA1c: 7.2 %  Age: 52  Sex: M"
    python analyze_report.py --value hba1c=7.2 --value age=52 --value sex=M
    python analyze_report.py report.txt --json result.json   # also save the result as JSON
    python analyze_report.py report.txt --no-ml             # rule-based checks only

DISCLAIMER: Screening aid only. It does not replace a diagnosis by a qualified doctor.
"""

import argparse
import json
import os
import sys
from datetime import datetime

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SEHATSETU_DIR = os.path.dirname(CURRENT_DIR)
for path in (CURRENT_DIR, os.path.join(SEHATSETU_DIR, "recommendation")):
    if path not in sys.path:
        sys.path.append(path)

from clinical_rules import (NORMAL, BORDERLINE, ABNORMAL, URGENT, SEVERITY_LABELS, run_clinical_rules)
from report_parser import parse_report, normalize_manual_values, display_name, unit_of
from report_reader import read_report, ReportReadError

try:
    from recommendation_system import get_recommendation
except ImportError:
    get_recommendation = None

# ML result confidence needed before it can add a finding on its own
ML_FLAG_THRESHOLD = 70.0

DECISIONS = {
    URGENT: ("URGENT - SEEK MEDICAL CARE TODAY",
             "One or more results are in a dangerous range. Contact a doctor or go to the nearest hospital today."),
    ABNORMAL: ("CONSULT A DOCTOR",
               "Some results are outside the normal range and suggest a condition that needs medical evaluation. "
               "Book an appointment within the next 1-2 weeks and take this report with you."),
    BORDERLINE: ("BORDERLINE - LIFESTYLE CHANGES AND RE-TEST",
                 "Some results are slightly outside the normal range. Follow the lifestyle advice below and "
                 "repeat the tests in 3-6 months, or earlier if your doctor advises."),
    NORMAL: ("NO ABNORMALITY FOUND",
             "All the values found in this report are within the normal range. Continue routine health check-ups."),
}


# -------------------------------------------------------------
# 1. DECISION MAKING
# -------------------------------------------------------------
def combine_with_models(findings, model_results):
    """Adds ML findings where a model flags risk that the rules did not, and notes disagreements."""
    notes = []
    for result in model_results:
        if result.get("status") != "ran":
            continue
        kb = result.get("kb_disease")
        rule_severity = max((f["severity"] for f in findings if f.get("kb_disease") == kb), default=NORMAL)
        prob = result["probability"]

        if result["positive"] and prob >= ML_FLAG_THRESHOLD and rule_severity == NORMAL:
            findings.append({
                "condition": result["label"], "parameter": "ML model", "value": f"{prob}%", "unit": "",
                "severity": BORDERLINE, "status": SEVERITY_LABELS[BORDERLINE],
                "message": f"The trained model estimates elevated risk ({prob}% probability, "
                           f"{result['coverage']}% of its inputs from the report). Discuss with a doctor.",
                "reference": "SehatSetu trained model", "kb_disease": kb,
            })
        elif not result["positive"] and rule_severity >= ABNORMAL:
            notes.append(f"{result['label']}: the ML model estimated low risk ({prob}%) but lab values are abnormal. "
                         f"The lab values take priority.")
    return notes


def summarize_conditions(findings):
    conditions = {}
    for f in findings:
        c = conditions.setdefault(f["condition"], {"condition": f["condition"], "severity": NORMAL,
                                                   "kb_disease": None, "evidence": []})
        c["severity"] = max(c["severity"], f["severity"])
        if f["severity"] > NORMAL:
            c["evidence"].append(f"{f['parameter']} {f['value']} {f['unit']}".strip() + f" - {f['message']}")
            c["kb_disease"] = c["kb_disease"] or f.get("kb_disease")
    for c in conditions.values():
        c["status"] = SEVERITY_LABELS[c["severity"]]
    return sorted(conditions.values(), key=lambda c: -c["severity"])


def build_guidance(conditions):
    guidance = []
    if get_recommendation is None:
        return guidance
    seen = set()
    for c in conditions:
        kb = c.get("kb_disease")
        if c["severity"] == NORMAL or not kb or kb in seen:
            continue
        seen.add(kb)
        info = get_recommendation(kb)
        if not info:
            continue
        guidance.append({
            "for": c["condition"],
            "food_prefer": info.get("food", {}).get("prefer", [])[:4],
            "food_limit": info.get("food", {}).get("limit", [])[:4],
            "exercise": info.get("exercise", {}).get("recommended", [])[:3],
            "lifestyle": info.get("lifestyle", [])[:3],
            "warning_signs": info.get("warning_signs", [])[:4],
            "when_to_seek_help": info.get("when_to_seek_help", [])[:3],
        })
    return guidance


def analyze_values(values, sources=None, use_ml=True):
    """Runs the full examination on parsed values and returns the analysis dict."""
    findings = run_clinical_rules(values)

    if use_ml:
        from model_bridge import run_models
        model_results = run_models(values)
    else:
        model_results = []
    notes = combine_with_models(findings, model_results)

    conditions = summarize_conditions(findings)
    overall = max((c["severity"] for c in conditions), default=NORMAL)
    decision, action = DECISIONS[overall]
    if not findings:
        decision = "NOT ENOUGH DATA"
        action = ("No supported test values were recognised in this report. Supported tests include blood sugar, "
                  "HbA1c, lipid profile, kidney & liver function, thyroid, CBC, blood pressure and BMI.")

    return {
        "analyzed_at": datetime.now().isoformat(timespec="seconds"),
        "decision": decision,
        "overall_severity": SEVERITY_LABELS[overall],
        "recommended_action": action,
        "conditions": conditions,
        "findings": findings,
        "extracted_values": values,
        "value_sources": sources or {},
        "model_results": model_results,
        "notes": notes,
        "guidance": build_guidance(conditions),
        "disclaimer": "This is an automated screening aid, not a medical diagnosis. "
                      "Always confirm results with a qualified doctor.",
    }


def analyze_report_text(text, use_ml=True):
    values, sources = parse_report(text)
    return analyze_values(values, sources, use_ml)


def analyze_report_file(path, use_ml=True):
    text, manual = read_report(path)
    if manual is not None:
        return analyze_values(normalize_manual_values(manual), None, use_ml)
    return analyze_report_text(text, use_ml)


# -------------------------------------------------------------
# 2. CONSOLE OUTPUT
# -------------------------------------------------------------
MARK = {NORMAL: "  OK ", BORDERLINE: " [!] ", ABNORMAL: " [!!]", URGENT: "[!!!]"}


def print_analysis(result):
    line = "=" * 70
    print("\n" + line)
    print("SEHATSETU - MEDICAL REPORT EXAMINATION")
    print(line)

    values = result["extracted_values"]
    print(f"\nValues recognised in the report ({len(values)}):")
    for key, val in values.items():
        shown = f"{val:g}" if isinstance(val, float) else str(val)
        print(f"   - {display_name(key)}: {shown} {unit_of(key)}".rstrip())

    print("\nTest-by-test examination:")
    for f in result["findings"]:
        print(f"  {MARK[f['severity']]} {f['parameter']:<24} {str(f['value']):>10} {f['unit']:<14} {f['message']}")

    ran = [m for m in result["model_results"] if m.get("status") == "ran"]
    others = [m for m in result["model_results"] if m.get("status") != "ran"]
    if result["model_results"]:
        print("\nMachine-learning models:")
        for m in ran:
            prob = m["probability"]
            verdict = "risk flagged" if prob >= ML_FLAG_THRESHOLD else "uncertain" if prob >= 50 else "low risk"
            print(f"   - {m['label']}: {verdict} ({prob}% probability, inputs from report {m['features_used']})")
        for m in others:
            print(f"   - {m.get('label', m['model'])}: not used - {m['reason']}")
    for note in result["notes"]:
        print(f"   * {note}")

    print("\n" + line)
    print(f"DECISION: {result['decision']}")
    print(line)
    print(result["recommended_action"])

    flagged = [c for c in result["conditions"] if c["severity"] > NORMAL]
    if flagged:
        print("\nConditions to discuss with your doctor:")
        for c in flagged:
            print(f"  {MARK[c['severity']]} {c['condition']} ({c['status']})")
            for e in c["evidence"]:
                print(f"         - {e}")

    for g in result["guidance"]:
        print(f"\nGuidance for {g['for']}:")
        for title, key in (("Prefer", "food_prefer"), ("Limit", "food_limit"), ("Exercise", "exercise"),
                           ("Lifestyle", "lifestyle"), ("Warning signs", "warning_signs"),
                           ("Seek help if", "when_to_seek_help")):
            if g[key]:
                print(f"   {title}:")
                for item in g[key]:
                    print(f"      - {item}")

    print("\n" + result["disclaimer"])
    print(line + "\n")


# -------------------------------------------------------------
# 3. INPUT HANDLING
# -------------------------------------------------------------
MANUAL_PROMPTS = [
    ("age", "Age (years)"), ("sex", "Sex (M/F)"), ("bp", "Blood pressure (e.g. 130/85)"),
    ("height", "Height (cm)"), ("weight", "Weight (kg)"),
    ("fasting_glucose", "Fasting blood glucose (mg/dL)"), ("hba1c", "HbA1c (%)"),
    ("total_cholesterol", "Total cholesterol (mg/dL)"), ("ldl", "LDL (mg/dL)"), ("hdl", "HDL (mg/dL)"),
    ("triglycerides", "Triglycerides (mg/dL)"), ("hemoglobin", "Haemoglobin (g/dL)"),
    ("creatinine", "Serum creatinine (mg/dL)"), ("urea", "Blood urea (mg/dL)"),
    ("alt", "ALT / SGPT (U/L)"), ("ast", "AST / SGOT (U/L)"), ("total_bilirubin", "Total bilirubin (mg/dL)"),
    ("tsh", "TSH (mIU/L)"), ("smoking", "Smoker? (yes/no)"),
]


def interactive_input():
    print("=" * 70)
    print("SEHATSETU - MEDICAL REPORT ANALYZER")
    print("=" * 70)
    print("How do you want to provide the report?")
    print("  1. Report file path (.pdf, .txt, .png/.jpg scan, .json)")
    print("  2. Paste the report text")
    print("  3. Type the test values one by one")
    choice = input("Choose 1, 2 or 3: ").strip()

    if choice == "1":
        return "file", input("Report file path: ").strip().strip('"')
    if choice == "2":
        print("Paste the report text. Type END on a new line when finished:")
        lines = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            if line.strip().upper() == "END":
                break
            lines.append(line)
        return "text", "\n".join(lines)

    print("Press Enter to skip any test you don't have.")
    raw = {}
    for key, prompt in MANUAL_PROMPTS:
        answer = input(f"  {prompt}: ").strip()
        if answer:
            raw[key] = answer
    return "values", raw


def parse_value_args(pairs):
    raw = {}
    for pair in pairs:
        if "=" not in pair:
            raise ValueError(f"--value must look like key=value (got '{pair}')")
        key, val = pair.split("=", 1)
        raw[key.strip()] = val.strip()
    return raw


def main():
    parser = argparse.ArgumentParser(description="Examine a medical report and make a screening decision.")
    parser.add_argument("report", nargs="?", help="Report file: .pdf, .txt, .png/.jpg (OCR) or .json of values")
    parser.add_argument("--text", help="Report text given directly")
    parser.add_argument("--value", action="append", default=[], metavar="KEY=VALUE",
                        help="A test value, e.g. --value hba1c=7.1 (can repeat)")
    parser.add_argument("--json", metavar="PATH", help="Also save the full result as JSON")
    parser.add_argument("--no-ml", action="store_true", help="Use only the clinical rules, not the ML models")
    args = parser.parse_args()

    use_ml = not args.no_ml
    try:
        if args.report:
            result = analyze_report_file(args.report, use_ml)
        elif args.text:
            result = analyze_report_text(args.text, use_ml)
        elif args.value:
            result = analyze_values(normalize_manual_values(parse_value_args(args.value)), None, use_ml)
        else:
            mode, data = interactive_input()
            if mode == "file":
                result = analyze_report_file(data, use_ml)
            elif mode == "text":
                result = analyze_report_text(data, use_ml)
            else:
                result = analyze_values(normalize_manual_values(data), None, use_ml)
    except (ReportReadError, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)

    print_analysis(result)

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False, default=str)
        print(f"Result saved to {args.json}")


if __name__ == "__main__":
    main()
