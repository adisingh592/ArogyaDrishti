==================================================
SEHATSETU - PARKINSON'S DISEASE TRAINING MODULE
==================================================

1. Dataset Source:
   Location: organized_datasets/Neurological/Parkinsons/
   Key Features: MDVP:Fo(Hz), MDVP:Fhi(Hz), MDVP:Flo(Hz), MDVP:Jitter(%), MDVP:Shimmer, HNR, RPDE, DFA, spread1, spread2, D2, PPE
   Target: status (1 = Parkinson's Disease, 0 = Healthy)

2. Algorithms Compared:
   - Logistic Regression
   - Decision Tree Classifier
   - Random Forest Classifier
   - Support Vector Machine (SVM)

3. Output Artifacts:
   - Best Model: SehatSetu/models/tabular/parkinsons/parkinsons_model.pkl
   - Preprocessor: SehatSetu/models/tabular/parkinsons/parkinsons_preprocessor.pkl
   - Evaluation Metrics: SehatSetu/results/tabular/parkinsons/metrics.txt
   - Confusion Matrix: SehatSetu/results/tabular/parkinsons/confusion_matrix.png
   - Comparison Table: SehatSetu/results/tabular/parkinsons/model_comparison.csv

4. How to Run:
   Double-click `train.bat` or run:
   python train.py
