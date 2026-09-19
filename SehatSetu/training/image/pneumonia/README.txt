==================================================
SEHATSETU - PNEUMONIA IMAGE TRAINING MODULE
==================================================

1. Dataset Source:
   Location: organized_datasets/Respiratory/Pneumonia/ (or chest_xray)
   Modalities: Chest X-Ray Images (PNG, JPEG)
   Target Classes: Normal vs Pneumonia

2. Neural Architecture:
   - Base Model: MobileNetV2 (Pretrained on ImageNet)
   - Input Dimensions: (224, 224, 3)
   - Classification Head: GlobalAveragePooling2D + Dense(128, ReLU) + Dropout(0.3) + Dense(Sigmoid/Softmax)
   - Optimizer: Adam (lr = 0.0001)

3. Output Artifacts:
   - Trained Model: SehatSetu/models/image/pneumonia/pneumonia_model.keras
   - Evaluation Metrics: SehatSetu/results/image/pneumonia/metrics.txt
   - Confusion Matrix: SehatSetu/results/image/pneumonia/confusion_matrix.png
   - Loss/Accuracy Curves: SehatSetu/results/image/pneumonia/training_history.png

4. How to Run:
   Double-click `train.bat` or run:
   python train.py
