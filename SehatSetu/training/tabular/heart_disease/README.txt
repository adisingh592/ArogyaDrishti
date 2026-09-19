==================================================
SEHATSETU - HEART DISEASE TRAINING MODULE
==================================================

1. Dataset Source:
   Location: organized_datasets/Cardiovascular/Heart_Disease/
   Datasets Supported:
     - heart_failure_clinical_records_dataset.csv
     - processed.cleveland.data
     - heart.dat (Statlog)
   Key Features: Age, Sex, CP (Chest Pain), Resting BP, Cholesterol, Ejection Fraction, Serum Creatinine, etc.
   Target: Heart Disease Indicator (0 = No Heart Disease, 1 = Heart Disease Presence / Event)

2. Algorithms Compared:
   - Logistic Regression
   - Decision Tree Classifier
   - Random Forest Classifier
   - Support Vector Machine (SVM)

3. Output Artifacts:
   - Best Model: SehatSetu/models/tabular/heart_disease/heart_disease_model.pkl
   - Preprocessor: SehatSetu/models/tabular/heart_disease/heart_disease_preprocessor.pkl
   - Evaluation Metrics: SehatSetu/results/tabular/heart_disease/metrics.txt
   - Confusion Matrix: SehatSetu/results/tabular/heart_disease/confusion_matrix.png
   - Comparison Table: SehatSetu/results/tabular/heart_disease/model_comparison.csv

4. How to Run:
   Double-click `train.bat` or run:
   python train.py
