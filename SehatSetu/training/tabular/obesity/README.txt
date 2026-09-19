==================================================
SEHATSETU - OBESITY & LIFESTYLE TRAINING MODULE
==================================================

1. Dataset Source:
   Location: organized_datasets/Endocrine_Metabolic/Obesity_and_Lifestyle/estimation+of+obesity+levels+based+on+eating+habits+and+physical+condition/
   Dataset: ObesityDataSet_raw_and_data_sinthetic.csv
   Key Features: Gender, Age, Height, Weight, family_history_with_overweight, FAVC, FCVC, NCP, CAEC, SMOKE, CH2O, SCC, FAF, TUE, CALC, MTRANS
   Target: NObeyesdad (7 Classes: Insufficient Weight, Normal Weight, Overweight Level I & II, Obesity Type I, II, III)

2. Algorithms Compared:
   - Logistic Regression
   - Decision Tree Classifier
   - Random Forest Classifier
   - Support Vector Machine (SVM)

3. Output Artifacts:
   - Best Model: SehatSetu/models/tabular/obesity/obesity_model.pkl
   - Preprocessor: SehatSetu/models/tabular/obesity/obesity_preprocessor.pkl
   - Evaluation Metrics: SehatSetu/results/tabular/obesity/metrics.txt
   - Confusion Matrix: SehatSetu/results/tabular/obesity/confusion_matrix.png
   - Comparison Table: SehatSetu/results/tabular/obesity/model_comparison.csv

4. How to Run:
   Double-click `train.bat` or run:
   python train.py
