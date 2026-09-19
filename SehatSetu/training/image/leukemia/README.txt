==================================================
SEHATSETU - LEUKEMIA IMAGE TRAINING MODULE
==================================================

1. Dataset Source:
   Location: organized_datasets/Hematology/Leukemia/luekemina
   Modalities: Microscopic Blood Cell Images (6,500+ Scans)
   Target Classes: Leukemia Cell Morphology (Original / Segmented Classes)

2. Neural Architecture:
   - Base Model: MobileNetV2 (Pretrained on ImageNet)
   - Input Dimensions: (224, 224, 3)
   - Classification Head: GlobalAveragePooling2D + Dense(128, ReLU) + Dropout(0.3) + Dense(Softmax/Sigmoid)
   - Optimizer: Adam (lr = 0.0001)

3. Output Artifacts:
   - Trained Model: SehatSetu/models/image/leukemia/leukemia_model.keras
   - Evaluation Metrics: SehatSetu/results/image/leukemia/metrics.txt
   - Confusion Matrix: SehatSetu/results/image/leukemia/confusion_matrix.png
   - Loss/Accuracy Curves: SehatSetu/results/image/leukemia/training_history.png

4. How to Run:
   Double-click `train.bat` or run:
   python train.py
