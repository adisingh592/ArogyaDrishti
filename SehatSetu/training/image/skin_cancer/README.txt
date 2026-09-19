==================================================
SEHATSETU - SKIN CANCER IMAGE TRAINING MODULE
==================================================

1. Dataset Source:
   Location: organized_datasets/Oncology_Dermatology/Skin_Cancer/skin cancer
   Modalities: HAM10000 Dermatoscopic Images (10,000+ Scans)
   Target Classes: Pigmented Skin Lesions (Benign vs Malignant Subtypes)

2. Neural Architecture:
   - Base Model: MobileNetV2 (Pretrained on ImageNet)
   - Input Dimensions: (224, 224, 3)
   - Classification Head: GlobalAveragePooling2D + Dense(128, ReLU) + Dropout(0.3) + Dense(Softmax/Sigmoid)
   - Optimizer: Adam (lr = 0.0001)

3. Output Artifacts:
   - Trained Model: SehatSetu/models/image/skin_cancer/skin_cancer_model.keras
   - Evaluation Metrics: SehatSetu/results/image/skin_cancer/metrics.txt
   - Confusion Matrix: SehatSetu/results/image/skin_cancer/confusion_matrix.png
   - Loss/Accuracy Curves: SehatSetu/results/image/skin_cancer/training_history.png

4. How to Run:
   Double-click `train.bat` or run:
   python train.py
