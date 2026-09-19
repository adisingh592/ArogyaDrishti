==================================================
SEHATSETU - BRAIN TUMOR MRI TRAINING MODULE
==================================================

1. Dataset Source:
   Location: organized_datasets/Neurological/Brain_Tumor/brain tumour
   Modalities: Brain MRI Scans (JPEG, PNG) - 3,200+ Scans
   Target Classes: Brain Tumor Subtypes / Tumor vs Healthy

2. Neural Architecture:
   - Base Model: MobileNetV2 (Pretrained on ImageNet)
   - Input Dimensions: (224, 224, 3)
   - Classification Head: GlobalAveragePooling2D + Dense(128, ReLU) + Dropout(0.3) + Dense(Softmax/Sigmoid)
   - Optimizer: Adam (lr = 0.0001)

3. Output Artifacts:
   - Trained Model: SehatSetu/models/image/brain_tumor/brain_tumor_model.keras
   - Evaluation Metrics: SehatSetu/results/image/brain_tumor/metrics.txt
   - Confusion Matrix: SehatSetu/results/image/brain_tumor/confusion_matrix.png
   - Loss/Accuracy Curves: SehatSetu/results/image/brain_tumor/training_history.png

4. How to Run:
   Double-click `train.bat` or run:
   python train.py
