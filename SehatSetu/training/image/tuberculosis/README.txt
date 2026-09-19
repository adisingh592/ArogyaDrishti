==================================================
SEHATSETU - TUBERCULOSIS IMAGE TRAINING MODULE
==================================================

1. Dataset Source:
   Location: organized_datasets/Respiratory/Tuberculosis/TB_Chest_Radiography_Database
   Modalities: Chest X-Ray Images (PNG) - 4,200+ Scans
   Target Classes: Normal vs Tuberculosis

2. Neural Architecture:
   - Base Model: MobileNetV2 (Pretrained on ImageNet)
   - Input Dimensions: (224, 224, 3)
   - Classification Head: GlobalAveragePooling2D + Dense(128, ReLU) + Dropout(0.3) + Dense(Sigmoid)
   - Optimizer: Adam (lr = 0.0001)

3. Output Artifacts:
   - Trained Model: SehatSetu/models/image/tuberculosis/tuberculosis_model.keras
   - Evaluation Metrics: SehatSetu/results/image/tuberculosis/metrics.txt
   - Confusion Matrix: SehatSetu/results/image/tuberculosis/confusion_matrix.png
   - Loss/Accuracy Curves: SehatSetu/results/image/tuberculosis/training_history.png

4. How to Run:
   Double-click `train.bat` or run:
   python train.py
