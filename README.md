# ArogyaDrishti (आरोग्यदृष्टि)
### Multi-Disease AI Screening, Clinical Classification & Health Recommendation Platform

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![React Version](https://img.shields.io/badge/React-19-61dafb.svg)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-8.3-646cff.svg)](https://vitejs.dev/)
[![Tailwind CSS](https://img.shields.io/badge/TailwindCSS-3.4-38bdf8.svg)](https://tailwindcss.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Deployment](https://img.shields.io/badge/Deploy-Vercel%20%2B%20Railway-000000.svg)]()

---

## 📌 Platform Overview

**ArogyaDrishti** (formerly SehatSetu) is an integrated, end-to-end AI healthcare screening platform. It ingests standard medical reports (PDF, digital documents, scanned photos), extracts clinical laboratory biomarkers automatically via OCR and regex parsing, routes them through an **Intelligent Meta-Classifier** to evaluate matching disease prediction models, and surfaces deterministic, evidence-based health recommendations.

```
       Medical Report (PDF / Image / TXT)
                       │
                       ▼
    [React 19 Frontend (Vercel) / DM Sans + Anton UI]
                       │  HTTP POST /api/analyze
                       ▼
    [Python Flask + Gunicorn Microservice (Railway)]
                       │
        ┌──────────────┴──────────────┐
        ▼                             ▼
 [Rule-Based Clinical Triage]    [Meta-Classifier Router]
 (Deterministic Reference Cuts)  (Affinity & Overlap Scoring)
        │                             │
        │                             ▼
        │                [Adaptive Population Imputation]
        │                (Age=45, BMI=24.2 default baselines)
        │                             │
        │                             ▼
        │                [Trained ML Model Ensembles]
        │                (Random Forest, Decision Tree, Logistic)
        │                             │
        └──────────────┬──────────────┘
                       ▼
          [Unified JSON Diagnostic Output]
          • Model Confidence & Influence Metrics
          • Clinical Flagging (Normal / Borderline / High)
          • Evidence-Based Guidance (WHO / ADA / AHA JSON KB)
```

---

## 📁 Repository Architecture

```text
ArogyaDrishti/
├── api.py                             # Production Flask REST API with Gunicorn & CORS
├── Procfile                           # Railway web dyno start command
├── railway.toml                       # Railway deployment & health check configuration
├── requirements.txt                   # Production backend Python dependencies
├── start_dev.bat                      # One-click Windows local development startup
├── .gitignore                         # Comprehensive ignore rules (Node, ML artifacts, logs)
│
├── frontend/                          # Modern React 19 + Vite + TailwindCSS Web Application
│   ├── index.html                     # Web entry point with Anton & DM Sans typography
│   ├── package.json                   # React, Vite, Tailwind, Radix UI dependencies
│   ├── tailwind.config.js             # Editorial color tokens & brutalist typography
│   ├── vite.config.js                 # Path aliases (@/*) and production build config
│   ├── vercel.json                    # SPA routing rewrite rules for clean URLs
│   └── src/
│       ├── App.jsx                    # Client-side router & AppContext wrapper
│       ├── context/
│       │   └── AppContext.jsx         # Global state & API transport layer
│       ├── components/
│       │   ├── Navbar.jsx             # Sticky glassmorphic navbar with active indicators
│       │   ├── Footer.jsx             # Institutional disclaimer & footer
│       │   ├── DisclaimerBar.jsx      # Top warning banner
│       │   └── ui/                    # Reusable shadcn/ui components (Button, Header-2)
│       └── pages/
│           ├── HomePage.jsx           # Bento showcase, comparison, & live model ticker
│           ├── UploadPage.jsx         # Step 1: Drag-and-drop report ingestion & sample loader
│           ├── AnalysisPage.jsx       # Step 2: Extracted parameter table & disease router
│           ├── ResultsPage.jsx        # Step 3: Screening metrics, model confidence, influence
│           └── GuidancePage.jsx       # Step 4: 3-tier actionable nutrition & clinical guidance
│
├── SehatSetu/
│   ├── models/                        # Pretrained models (.pkl) & preprocessors
│   │   ├── tabular/                   # Diabetes, Kidney, Liver, Thyroid, Heart, Stroke
│   │   ├── image/                     # Tuberculosis, Brain Tumor, Malaria, Leukemia
│   │   └── eeg/                       # Neurological signal model artifacts
│   ├── report_analysis/               # Inference & diagnostic evaluation engine
│   │   ├── analyze_report.py          # Unified triage decision & report examination engine
│   │   ├── model_bridge.py            # Meta-Classifier Router & Adaptive Population Imputation
│   │   ├── clinical_rules.py          # Deterministic clinical reference cutoffs
│   │   ├── report_reader.py           # Multi-format document reader (PDF, TXT, OCR)
│   │   └── report_parser.py           # Biomarker regex & unit normalization
│   └── recommendation/
│       ├── disease_information.json   # 34-disease clinical knowledge base (WHO, ADA, AHA)
│       └── recommendation_system.py   # Deterministic recommendation engine
│
└── ML_Project/                        # Supplementary experimentation & test suites
```

---

## 🧠 Core Engineering Features

### 1. Intelligent Meta-Classifier Router
Standard clinical lab documents often focus on specific panels (e.g., Lipid profile or Renal panel) without patient demographics. Instead of hard-failing or skipping models, ArogyaDrishti uses an **Affinity Scoring Engine**:
* Evaluates incoming biomarkers against each model's primary and secondary clinical signatures.
* Activates all matching organ-system models whose primary markers are detected.
* **Fallback Guarantee**: If no primary biomarker matches directly, the engine ranks models by feature overlap and triggers the closest matching models. **Models evaluated is never 0**.

### 2. Adaptive Population Imputation
To prevent inference crashes when reports lack non-laboratory context:
* **Missing Demographics**: Applies standard healthy population baselines (`Age: 45.0`, `BMI: 24.2`, `Sex: neutral/mode`).
* **Unmeasured Tests**: Filled via the model's trained median imputer.
* **Transparent Logging**: Assumed values are reported directly on the UI (e.g. `Defaults: Age (default 45), BMI (default 24.2)`).

### 3. Dual-Layer Safety Triage
* **Layer 1 (Deterministic Clinical Rules)**: Evaluates lab values strictly against standard diagnostic ranges (Normal, Borderline, Abnormal, Urgent).
* **Layer 2 (Machine Learning Ensembles)**: Computes multivariate probabilities across 10+ clinical indicators.
* If a machine learning model estimates low probability but a biomarker exceeds an urgent clinical cutoff, the clinical rule takes precedence for patient safety.

### 4. Deterministic Clinical Guidance
Dietary guidelines, activity contraindications, and emergency red-flags are rendered strictly from a curated clinical database (`disease_information.json`) sourced from recognized health authorities (WHO, CDC, ADA, NHS, AHA), eliminating generative hallucination risk.

---

## 📊 Model Coverage & Validation

Scores measured on a held-out 20% test split:

| Organ System | Disease / Condition | Best Architecture | Test Samples | Accuracy | Primary Inputs |
| :--- | :--- | :--- | --:| :---: | :--- |
| **Endocrine** | Thyroid (Hypothyroid) | Decision Tree | 633 | **98.7%** | TSH, Free T4, T3, Age |
| **Endocrine** | Diabetes Mellitus | Random Forest (BRFSS) | 14,139 | **75.0%** | Glucose, HbA1c, BMI, BP, Cholesterol |
| **Renal** | Chronic Kidney Disease | Logistic Regression | 80 | **92.5%** | Serum Creatinine, Urea, Albumin, BP |
| **Hepatic** | Liver Disease (ILPD) | Random Forest | 117 | **74.4%** | ALT, AST, Total Bilirubin, Albumin |
| **Cardiovascular** | Heart Failure Risk | Random Forest | 60 | **85.0%** | Ejection Fraction, CPK, BP, Cholesterol |
| **Neurological** | Cerebrovascular Stroke | Decision Tree | 1,022 | **82.8%** | Blood Glucose, Systolic BP, BMI, Age |
| **Hematology** | Clinical Anemia | Logistic Regression | 21 | **96.0%** | Hemoglobin, Hematocrit (PCV), RBC |
| **Respiratory** | Tuberculosis | MobileNetV2 (224×224) | 840 | **93.0%** | Chest Radiograph (X-Ray) |
| **Neurological** | Brain Tumor | MobileNetV2 (224×224) | 574 | **74.0%** | Brain MRI Scans |

---

## 🚀 Local Development Setup

### Prerequisites
* **Python 3.8+** (recommended Python 3.10 or 3.11)
* **Node.js 18+** and **pnpm** (or npm)

### Option A: One-Click Startup (Windows)
Double-click `start_dev.bat` in the project root. This automatically:
1. Launches the Flask backend on `http://localhost:8000`.
2. Launches the React Vite frontend on `http://localhost:5173`.

### Option B: Manual Startup

#### 1. Start the Flask Backend API
```bash
# In the project root:
pip install -r requirements.txt
python api.py
```
*API will be listening at `http://localhost:8000` (Healthcheck: `http://localhost:8000/api/health`)*

#### 2. Start the React Frontend
```bash
cd frontend
pnpm install
pnpm run dev
```
*Web UI will be live at `http://localhost:5173`*

---

## 🌐 Production Deployment Guide

### Backend: Railway Deployment
1. Connect the repository (`adisingh592/ArogyaDrishti`) to **[Railway](https://railway.app)**.
2. Railway detects `railway.toml`, `Procfile`, and `requirements.txt` automatically.
3. In **Settings** $\rightarrow$ **Networking**, click **Generate Domain** to get your public backend URL:
   ```text
   https://arogyadrishti-production.up.railway.app
   ```
4. Verify by opening `/api/health` in your browser.

### Frontend: Vercel Deployment
1. Import the repository on **[Vercel](https://vercel.com)**.
2. Set **Root Directory** to `frontend`.
3. Framework Preset: **Vite** (auto-detected).
4. Add the Environment Variable in **Settings** $\rightarrow$ **Environment Variables**:
   * **Key:** `VITE_API_URL`
   * **Value:** `https://your-railway-url.up.railway.app` *(without trailing slash)*
5. In **Settings** $\rightarrow$ **Deployment Protection**, disable Vercel Authentication for public access.
6. Deploy!

---

## 📡 API Specification

### `POST /api/analyze`
Accepts `multipart/form-data` with a report file or `application/json` with raw text:

**Request:**
```bash
curl -X POST https://arogyadrishti-production.up.railway.app/api/analyze \
  -F "file=@sample_report.pdf"
```

**Response Payload:**
```json
{
  "analyzed_at": "2026-11-13T14:30:00",
  "decision": "CONSULT A DOCTOR",
  "overall_severity": "ABNORMAL",
  "recommended_action": "Some results are outside the normal range...",
  "extracted_values": {
    "fasting_glucose": 142.0,
    "hba1c": 6.9,
    "total_cholesterol": 214.0,
    "hemoglobin": 13.1,
    "creatinine": 0.9
  },
  "findings": [
    {
      "parameter": "Fasting glucose",
      "value": 142.0,
      "unit": "mg/dL",
      "reference": "70 – 99",
      "status": "ABNORMAL"
    }
  ],
  "model_results": [
    {
      "model": "diabetes",
      "label": "Diabetes Risk Model",
      "status": "ran",
      "probability": 78.4,
      "positive": true,
      "features_used": "5/21",
      "coverage": 23.8,
      "assumptions": ["Age (default 45)", "BMI (default 24.2)"]
    }
  ],
  "guidance": [
    {
      "for": "Diabetes",
      "food_prefer": ["Vegetables and leafy greens", "Whole grains"],
      "food_limit": ["Sugary drinks and sweets", "Refined flour"],
      "exercise": ["Brisk walking 30 mins daily"],
      "lifestyle": ["Sleep 7 to 9 hours nightly"],
      "warning_signs": ["Constant thirst", "Unexplained weight loss"]
    }
  ]
}
```

---

## ⚠️ Medical Safety & Disclaimer

> **IMPORTANT CLINICAL NOTICE:**  
> ArogyaDrishti is an **academic AI screening and educational tool**. It is **not** a diagnostic device, clinical laboratory, or a substitute for professional medical consultation.  
> * Predictions and risk percentages are probabilistic screening indicators only.  
> * Never begin, alter, or discontinue prescription medications based on system outputs.  
> * Always review medical reports and screening indicators with a qualified medical practitioner.  
> * In case of acute, severe, or emergency symptoms, immediately contact local emergency healthcare services.
