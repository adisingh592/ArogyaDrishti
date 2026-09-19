==================================================
SEHATSETU - ADDITIONAL TABULAR TRAINING MODULE
==================================================

1. Dataset Source:
   Location: organized_datasets/Hematology/Anemia/ OR Obstetrics_Gynecology/ OR Oncology_Dermatology/
   Datasets Supported:
     - anemia_dataset.csv
     - Maternal Health Risk Data Set.csv
     - wdbc.data (Breast Cancer Wisconsin Diagnostic)
   Target: Disease Presence / Risk Level

2. Algorithms Compared:
   - Logistic Regression
   - Decision Tree Classifier
   - Random Forest Classifier
   - Support Vector Machine (SVM)

3. Output Artifacts:
   - Best Model: SehatSetu/models/tabular/other/other_model.pkl
   - Preprocessor: SehatSetu/models/tabular/other/other_preprocessor.pkl
   - Evaluation Metrics: SehatSetu/results/tabular/other/metrics.txt
   - Confusion Matrix: SehatSetu/results/tabular/other/confusion_matrix.png
   - Comparison Table: SehatSetu/results/tabular/other/model_comparison.csv

4. How to Run:
   Double-click `train.bat` or run:
   python train.py
