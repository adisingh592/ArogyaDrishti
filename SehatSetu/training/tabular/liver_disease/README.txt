==================================================
SEHATSETU - LIVER DISEASE TRAINING MODULE
==================================================

1. Dataset Source:
   Location: organized_datasets/Hepatic_System/Liver_Disease/ilpd+indian+liver+patient+dataset/
   Dataset: Indian Liver Patient Dataset (ILPD).csv
   Key Features: Age, Gender, Total Bilirubin, Direct Bilirubin, Alkaline Phosphotase, Alamine Aminotransferase, Aspartate Aminotransferase, Total Proteins, Albumin, A/G Ratio
   Target: Liver Disease Indicator (1 = Liver Patient, 0 = Non-liver Patient)

2. Algorithms Compared:
   - Logistic Regression
   - Decision Tree Classifier
   - Random Forest Classifier
   - Support Vector Machine (SVM)

3. Output Artifacts:
   - Best Model: SehatSetu/models/tabular/liver_disease/liver_disease_model.pkl
   - Preprocessor: SehatSetu/models/tabular/liver_disease/liver_disease_preprocessor.pkl
   - Evaluation Metrics: SehatSetu/results/tabular/liver_disease/metrics.txt
   - Confusion Matrix: SehatSetu/results/tabular/liver_disease/confusion_matrix.png
   - Comparison Table: SehatSetu/results/tabular/liver_disease/model_comparison.csv

4. How to Run:
   Double-click `train.bat` or run:
   python train.py
