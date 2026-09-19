# SehatSetu (सेहतसेतु)
### AI-Based Multi-Disease Detection, Classification & Health Guidance System

---

## 📌 1. Project Overview

**SehatSetu** is an end-to-end artificial intelligence healthcare platform designed for **Multi-Disease Detection, Classification, and Evidence-Based Health Guidance**. 

The system bridges clinical diagnostics and patient lifestyle management by uniting three pillars:
1. **Multi-Modal Diagnostic AI**: Machine learning and deep learning pipelines capable of analyzing tabular health indicators, medical imaging (X-rays, dermoscopy, cell smears), and physiological time-series signals.
2. **Standardized Model Evaluation**: Systematic benchmarking of multiple algorithms (Logistic Regression, Decision Trees, Random Forests, Support Vector Machines, MobileNetV2 CNNs) with automated best-model selection.
3. **Deterministic Health Guidance**: A rule-based clinical recommendation engine providing lifestyle modifications, dietary advice, exercise cautions, and emergency warning signs without hallucination risk.

---

## 🔄 2. End-to-End System Workflow

```
┌─────────────────────────────────────────────────────────┐
│              ORGANIZED MEDICAL DATASETS                 │
│         (Tabular CSVs, X-Rays, Dermoscopy, EEG)         │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│               DISEASE-SPECIFIC TRAINING                 │
│        (Data Cleaning, Scaling, Model Training)         │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│            MODEL EVALUATION & BENCHMARKING              │
│       (Accuracy, Precision, Recall, F1, Conf Matrix)   │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│                   BEST MODEL SELECTION                  │
│       (Saved to models/ & Results saved to results/)    │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│                  PREDICTION SUBSYSTEM                   │
│         (Input Preprocessing -> Model Inference)        │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│               RECOMMENDATION ENGINE                     │
│    (Structured Knowledge Base: Diet, Lifestyle, Risks)  │
└────────────────────────────┬────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────┐
│                 FINAL APPLICATION UI                    │
│             (Web Dashboard / Clinical GUI)              │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 3. Project Directory Structure

```text
SehatSetu/
│
├── models/                               # Trained model artifacts (.pkl, .keras)
│   ├── tabular/                          # Tabular models (diabetes, heart, kidney, etc.)
│   ├── image/                            # Vision models (pneumonia, TB, skin cancer, etc.)
│   └── eeg/                              # EEG time-series models
│
├── training/                             # Standalone training pipelines per disease
│   ├── tabular/
│   │   ├── diabetes/                     # train.py, train.bat, README.txt
│   │   ├── heart_disease/                # train.py, train.bat, README.txt
│   │   ├── kidney_disease/               # train.py, train.bat, README.txt
│   │   ├── liver_disease/                # train.py, train.bat, README.txt
│   │   ├── stroke/                       # train.py, train.bat, README.txt
│   │   ├── parkinsons/                   # train.py, train.bat, README.txt
│   │   ├── alzheimers/                   # train.py, train.bat, README.txt
│   │   ├── obesity/                      # train.py, train.bat, README.txt
│   │   ├── thyroid/                      # train.py, train.bat, README.txt
│   │   └── other/                        # train.py, train.bat, README.txt
│   │
│   ├── image/
│   │   ├── pneumonia/                    # train.py, train.bat, README.txt
│   │   ├── tuberculosis/                 # train.py, train.bat, README.txt
│   │   ├── skin_cancer/                  # train.py, train.bat, README.txt
│   │   ├── brain_tumor/                  # train.py, train.bat, README.txt
│   │   ├── malaria/                      # train.py, train.bat, README.txt
│   │   ├── leukemia/                     # train.py, train.bat, README.txt
│   │   └── other/                        # train.py, train.bat, README.txt
│   │
│   └── eeg/                              # train.py, train.bat, README.txt
│
├── results/                              # Evaluation metrics & visualizations
│   ├── tabular/                          # metrics.txt, confusion_matrix.png, model_comparison.csv
│   ├── image/                            # metrics.txt, confusion_matrix.png, training_history.png
│   └── eeg/                              # metrics.txt, confusion_matrix.png, model_comparison.csv
│
├── prediction/                           # Unified inference templates
│   ├── tabular_prediction.py             # Inference pipeline for tabular data
│   ├── image_prediction.py               # Inference pipeline for medical imagery
│   └── README.txt
│
├── recommendation/                       # Rule-based health advisory subsystem
│   ├── recommendation_system.py          # Core recommendation engine
│   ├── disease_information.json          # 34+ clinical condition knowledge base
│   ├── test_recommendation_system.py     # Automated test suite
│   └── README.txt
│
├── data/
│   └── dataset_report.csv                # Dataset inventory and structural audit report
│
├── app/
│   └── README.txt                        # Frontend / Web Application placeholder
│
├── requirements.txt                      # Project Python dependencies
└── README.md                             # Comprehensive project documentation
```

---

## 📊 4. Dataset Source & Safety Policy

All training pipelines dynamically read from the organized dataset store:
```
E:\multidisease prdiction\organized_datasets\
```

### Dataset Safety Rules:
* The original datasets are **NEVER modified, resized, renamed, or moved**.
* Missing values and feature scaling are processed **in-memory** during script execution.
* The original dataset store remains the Single Source of Truth for raw data.

---

## ⚙️ 5. Machine Learning Architecture

### A. Tabular Disease Models
For structured clinical records (blood panels, demographic metrics, vital signs), each disease script evaluates:
1. **Logistic Regression**: Linear baseline with calibrated probabilities.
2. **Decision Tree Classifier**: Interpretable rule-based splitting.
3. **Random Forest Classifier**: Ensemble of bagging decision trees for high non-linear accuracy.
4. **Support Vector Classifier (SVM)**: Maximum-margin hyperplane classification.

**Evaluation & Selection**:
* Models are benchmarked on **Accuracy, Precision, Recall, and F1-Score**.
* The best-performing model is automatically serialized as `<disease>_model.pkl` along with `<disease>_preprocessor.pkl`.

### B. Medical Image Models (Deep Learning)
For medical scans (X-rays, MRI, cell images), transfer learning is implemented using **MobileNetV2**:
* Pre-trained on ImageNet for rich feature extraction.
* Lightweight footprint (~14M parameters) ideal for real-time clinical edge devices.
* Global Average Pooling, Dropout regularization, and Dense classification head.
* Saves final model as `<disease>_model.keras` and training history curves.

### C. EEG Signal Models
* Extracts multi-channel spectral frequency features across Delta, Theta, Alpha, Beta, and Gamma bands.
* Evaluates Random Forest and SVM classifiers to detect neurological events and seizures.

---

## 🚀 6. How to Train Models

Each disease folder is self-contained. You can train any model individually when ready:

### Tabular Training:
1. Open terminal or file explorer to the desired disease folder:
   ```bash
   cd SehatSetu/training/tabular/diabetes/
   ```
2. Run the batch file or python script:
   ```bash
   train.bat
   # or
   python train.py
   ```

### Image Training:
1. Navigate to the image disease folder:
   ```bash
   cd SehatSetu/training/image/tuberculosis/
   ```
2. Run the batch file or python script:
   ```bash
   train.bat
   # or
   python train.py
   ```

---

## 🩺 7. Health Recommendation Subsystem

Medical recommendations require deterministic safety. SehatSetu uses a structured clinical knowledge base (`disease_information.json`) sourced from recognized healthcare bodies (WHO, CDC, NHS, ADA, AHA).

For every predicted disease, the recommendation engine provides:
- **Clinical Description & Common Symptoms**
- **Dietary Recommendations** (*Foods to Prefer vs. Foods to Limit*)
- **Exercise Guidelines & Contraindications**
- **Lifestyle Habits & Sleep Hygiene**
- **Home & Clinical Monitoring Protocols**
- **Red-Flag Warning Signs & Emergency Action Guidance**

### ⚠️ Strict Medical Disclaimer
> **IMPORTANT**: SehatSetu is an AI-assisted research and guidance platform. It **DOES NOT** prescribe medications, adjust dosages, or replace qualified medical consultation. Users are always instructed to consult certified medical professionals for clinical diagnosis and treatment.

---

## 🎓 8. College Viva & Technical Discussion Highlights

1. **Why separate training folders per disease?**
   * *Answer*: Decouples dependencies, enables independent tuning, prevents codebase bloat, and simplifies debugging and demonstration during viva.
2. **Why use F1-Score for model selection over simple Accuracy?**
   * *Answer*: Medical datasets often suffer from class imbalance (e.g. fewer stroke cases than normal). F1-Score balances Precision and Recall, avoiding biased high accuracy on majority classes.
3. **Why MobileNetV2 for Medical Images?**
   * *Answer*: MobileNetV2 utilizes depthwise separable convolutions, delivering high accuracy with low computational and memory overhead, making it suitable for deployment in clinic workstations.
4. **Why is the recommendation system rule-based instead of LLM-based?**
   * *Answer*: LLMs can hallucinate medical dosages and contraindicated diets. Rule-based knowledge systems guarantee 100% clinically verified, deterministic, and safe medical guidance.
