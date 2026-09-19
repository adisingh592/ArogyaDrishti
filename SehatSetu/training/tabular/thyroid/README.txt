==================================================
SEHATSETU - THYROID DISEASE TRAINING MODULE
==================================================

1. Dataset Source:
   Location: organized_datasets/Endocrine_Metabolic/Thyroid_Disease/thyroid+disease (1)/
   Dataset: hypothyroid.data
   Key Features: Age, Sex, On Thyroxine, Query on Thyroxine, On Antithyroid Meds, Sick, Pregnant, Thyroid Surgery, I131 Treatment, TSH, T3, TT4, T4U, FTI, etc.
   Target: Thyroid Condition (1 = Hypothyroid/Sick, 0 = Negative/Normal)

2. Algorithms Compared:
   - Logistic Regression
   - Decision Tree Classifier
   - Random Forest Classifier
   - Support Vector Machine (SVM)

3. Output Artifacts:
   - Best Model: SehatSetu/models/tabular/thyroid/thyroid_model.pkl
   - Preprocessor: SehatSetu/models/tabular/thyroid/thyroid_preprocessor.pkl
   - Evaluation Metrics: SehatSetu/results/tabular/thyroid/metrics.txt
   - Confusion Matrix: SehatSetu/results/tabular/thyroid/confusion_matrix.png
   - Comparison Table: SehatSetu/results/tabular/thyroid/model_comparison.csv

4. How to Run:
   Double-click `train.bat` or run:
   python train.py
