==================================================
SEHATSETU - CHRONIC KIDNEY DISEASE TRAINING MODULE
==================================================

1. Dataset Source:
   Location: organized_datasets/Renal_System/Chronic_Kidney_Disease/Chronic_Kidney_Disease/chronic_kidney_disease.arff
   Key Features: Age, Blood Pressure, Specific Gravity, Albumin, Sugar, RBC, Pus Cells, Serum Creatinine, Sodium, Potassium, Hemoglobin, etc.
   Target: class (ckd = 1, notckd = 0)

2. Algorithms Compared:
   - Logistic Regression
   - Decision Tree Classifier
   - Random Forest Classifier
   - Support Vector Machine (SVM)

3. Output Artifacts:
   - Best Model: SehatSetu/models/tabular/kidney_disease/kidney_disease_model.pkl
   - Preprocessor: SehatSetu/models/tabular/kidney_disease/kidney_disease_preprocessor.pkl
   - Evaluation Metrics: SehatSetu/results/tabular/kidney_disease/metrics.txt
   - Confusion Matrix: SehatSetu/results/tabular/kidney_disease/confusion_matrix.png
   - Comparison Table: SehatSetu/results/tabular/kidney_disease/model_comparison.csv

4. How to Run:
   Double-click `train.bat` or run:
   python train.py
