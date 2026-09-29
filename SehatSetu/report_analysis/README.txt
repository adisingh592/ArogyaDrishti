==================================================
SEHATSETU - MEDICAL REPORT ANALYSIS
==================================================

1. Overview:
   Reads a patient's medical / lab report, examines every test value and makes a
   screening decision with health guidance.

2. How to run:
   python analyze_report.py                         (interactive)
   python analyze_report.py sample_report.txt       (.txt / .pdf / .png / .jpg / .json)
   python analyze_report.py --text "HbA1c 7.2 %  Age 52  Sex M"
   python analyze_report.py --value hba1c=7.2 --value sex=M --value age=52
   python analyze_report.py report.pdf --json result.json
   python analyze_report.py report.pdf --no-ml       (clinical rules only)

   JSON input example: {"age": 52, "sex": "M", "bp": "142/92", "hba1c": 7.2, "creatinine": 1.6}

3. Files:
   - analyze_report.py : entry point, decision making, console output
   - report_reader.py  : text from PDF (pypdf), images (pytesseract OCR), txt, json
   - report_parser.py  : finds ~40 lab tests, converts units (mmol/L, umol/L, g/L, lakh)
   - clinical_rules.py : reference-range checks (ADA, ACC/AHA, NCEP, WHO, KDIGO, ATA)
   - model_bridge.py   : maps report values to the trained tabular models and runs them
   - sample_report.txt : example report (fictional patient) for testing

4. Flow:
   Report file / text / values
         |
   Extract text (PDF / OCR)  ->  Parse test values + convert units
         |
   Clinical rules (reference ranges)   +   Trained ML models (if enough inputs)
         |
   Decision: URGENT / CONSULT A DOCTOR / BORDERLINE / NO ABNORMALITY / NOT ENOUGH DATA
         |
   Guidance from recommendation/recommendation_system.py

5. Decision logic:
   - Each test gets a severity: Normal, Borderline, Abnormal, Urgent.
   - The overall decision is the highest severity found.
   - The lab-value rules take priority. An ML model can add a Borderline flag
     (when >= 70% probability) but can never clear an abnormal lab value.
   - A model runs only when the report has its key inputs and enough of its
     features. The output shows how many model inputs came from the report.

6. Known model limitations:
   - Diabetes model uses survey answers (BRFSS), so lab reports rarely have enough inputs.
   - Heart model predicts heart-failure mortality and needs ejection fraction (echo report).
   - Liver model (ILPD) gives ~60% risk even for normal values; the rules decide instead.
   - Thyroid model needs total T4; FTI is estimated from it.

7. Disclaimer:
   Screening aid only. It does not diagnose disease. Always confirm with a doctor.
==================================================
