==================================================
SEHATSETU - ALZHEIMER'S DISEASE TRAINING MODULE
==================================================

1. Dataset Source:
   Location: organized_datasets/Neurological/Alzheimers_Disease/alhezhimer/
   Dataset: ML_transform_alz.csv
   Key Features: Cognitive, lifestyle, and clinical health indicators
   Target: Clinical indicator / Alzheimer risk factor

2. Algorithms Compared:
   - Logistic Regression
   - Decision Tree Classifier
   - Random Forest Classifier
   - Support Vector Machine (SVM)

3. Output Artifacts:
   - Best Model: SehatSetu/models/tabular/alzheimers/alzheimers_model.pkl
   - Preprocessor: SehatSetu/models/tabular/alzheimers/alzheimers_preprocessor.pkl
   - Evaluation Metrics: SehatSetu/results/tabular/alzheimers/metrics.txt
   - Confusion Matrix: SehatSetu/results/tabular/alzheimers/confusion_matrix.png
   - Comparison Table: SehatSetu/results/tabular/alzheimers/model_comparison.csv

4. How to Run:
   Double-click `train.bat` or run:
   python train.py
