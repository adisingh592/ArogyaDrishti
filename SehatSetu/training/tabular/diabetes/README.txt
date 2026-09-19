==================================================
SEHATSETU - DIABETES TRAINING MODULE
==================================================

1. Dataset Source:
   Location: organized_datasets/Endocrine_Metabolic/Diabetes/diabetes health indicator/
   Features: HighBP, HighChol, BMI, Smoker, Stroke, HeartDiseaseorAttack, PhysActivity, GenHlth, Age, etc.
   Target: Diabetes_binary (0 = No Diabetes, 1 = Diabetes)

2. Algorithms Compared:
   - Logistic Regression
   - Decision Tree Classifier
   - Random Forest Classifier
   - Support Vector Machine (SVM)

3. Output Artifacts:
   - Best Model: SehatSetu/models/tabular/diabetes/diabetes_model.pkl
   - Preprocessor: SehatSetu/models/tabular/diabetes/diabetes_preprocessor.pkl
   - Evaluation Metrics: SehatSetu/results/tabular/diabetes/metrics.txt
   - Confusion Matrix: SehatSetu/results/tabular/diabetes/confusion_matrix.png
   - Comparison Table: SehatSetu/results/tabular/diabetes/model_comparison.csv

4. How to Run:
   Double-click `train.bat` or run:
   python train.py
