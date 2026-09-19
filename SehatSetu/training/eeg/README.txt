==================================================
SEHATSETU - EEG / TIME-SERIES TRAINING MODULE
==================================================

1. Dataset Source:
   Location: organized_datasets/Neurological/ (EEG / Time-series Signal recordings)
   Features: Multi-channel EEG spectral signal features (Delta, Theta, Alpha, Beta, Gamma)
   Target: Neurological Event / Anomaly / Seizure Indicator

2. Algorithms Compared:
   - Logistic Regression
   - Decision Tree Classifier
   - Random Forest Classifier
   - Support Vector Machine (SVM)

3. Output Artifacts:
   - Best Model: SehatSetu/models/eeg/eeg_model.pkl
   - Preprocessor: SehatSetu/models/eeg/eeg_preprocessor.pkl
   - Evaluation Metrics: SehatSetu/results/eeg/metrics.txt
   - Confusion Matrix: SehatSetu/results/eeg/confusion_matrix.png
   - Comparison Table: SehatSetu/results/eeg/model_comparison.csv

4. How to Run:
   Double-click `train.bat` or run:
   python train.py
