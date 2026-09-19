==================================================
SEHATSETU - ADDITIONAL IMAGE TRAINING MODULE
==================================================

1. Dataset Source:
   Location: organized_datasets/
   Supports automated image discovery from subdirectories.

2. Neural Architecture:
   - Base Model: MobileNetV2 (Pretrained on ImageNet)
   - Input Dimensions: (224, 224, 3)
   - Classification Head: GlobalAveragePooling2D + Dense(128, ReLU) + Dropout(0.3) + Dense(Softmax/Sigmoid)
   - Optimizer: Adam (lr = 0.0001)

3. Output Artifacts:
   - Trained Model: SehatSetu/models/image/other/other_image_model.keras
   - Evaluation Metrics: SehatSetu/results/image/other/metrics.txt
   - Confusion Matrix: SehatSetu/results/image/other/confusion_matrix.png
   - Loss/Accuracy Curves: SehatSetu/results/image/other/training_history.png

4. How to Run:
   Double-click `train.bat` or run:
   python train.py
