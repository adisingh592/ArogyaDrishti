==================================================
SEHATSETU - PREDICTION SUBSYSTEM
==================================================

1. Overview:
   This module provides inference pipelines for tabular and medical image models, seamlessly passing predictions and confidence scores to the rule-based Health Recommendation System.

2. Files:
   - tabular_prediction.py: Loads .pkl models + preprocessors for tabular diseases and predicts clinical outcome.
   - image_prediction.py: Loads .keras MobileNetV2 models for image diseases and predicts disease class.

3. Flow:
   Patient Input / Image
         ↓
   Load Trained Model from SehatSetu/models/
         ↓
   Preprocess Input (Scale / Normalize)
         ↓
   Predict Outcome & Confidence (%)
         ↓
   Pass to SehatSetu/recommendation/recommendation_system.py
         ↓
   Display Safe Clinical & Lifestyle Guidance
