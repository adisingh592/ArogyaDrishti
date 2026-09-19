==================================================
SEHATSETU - MALARIA CELL IMAGE TRAINING MODULE
==================================================

1. Dataset Source:
   Location: organized_datasets/Infectious_Diseases/Malaria/malaria/cell_images/
   Modalities: Microscopic Blood Smear Cell Images (PNG) - 55,000+ Cells
   Target Classes: Parasitized vs Uninfected

2. Neural Architecture:
   - Base Model: MobileNetV2 (Pretrained on ImageNet)
   - Input Dimensions: (224, 224, 3)
   - Classification Head: GlobalAveragePooling2D + Dense(128, ReLU) + Dropout(0.3) + Dense(Sigmoid)
   - Optimizer: Adam (lr = 0.0001)

3. Output Artifacts:
   - Trained Model: SehatSetu/models/image/malaria/malaria_model.keras
   - Evaluation Metrics: SehatSetu/results/image/malaria/metrics.txt
   - Confusion Matrix: SehatSetu/results/image/malaria/confusion_matrix.png
   - Loss/Accuracy Curves: SehatSetu/results/image/malaria/training_history.png

4. How to Run:
   Double-click `train.bat` or run:
   python train.py
