==================================================
SEHATSETU - STROKE TRAINING MODULE
==================================================

1. Dataset Source:
   Location: organized_datasets/Cardiovascular/Stroke/heart stroke/
   Dataset: healthcare-dataset-stroke-data.csv
   Key Features: Gender, Age, Hypertension, Heart Disease, Ever Married, Work Type, Residence Type, Avg Glucose Level, BMI, Smoking Status
   Target: stroke (1 = Stroke Event, 0 = No Stroke)

2. Algorithms Compared:
   - Logistic Regression
   - Decision Tree Classifier
   - Random Forest Classifier
   - Support Vector Machine (SVM)

3. Output Artifacts:
   - Best Model: SehatSetu/models/tabular/stroke/stroke_model.pkl
   - Preprocessor: SehatSetu/models/tabular/stroke/stroke_preprocessor.pkl
   - Evaluation Metrics: SehatSetu/results/tabular/stroke/metrics.txt
   - Confusion Matrix: SehatSetu/results/tabular/stroke/confusion_matrix.png
   - Comparison Table: SehatSetu/results/tabular/stroke/model_comparison.csv

4. How to Run:
   Double-click `train.bat` or run:
   python train.py
