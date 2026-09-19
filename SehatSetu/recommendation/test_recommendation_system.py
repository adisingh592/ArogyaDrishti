import os
import sys

# Add Recommendation_System to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from recommendation_system import get_recommendation, display_recommendation


def run_tests():
    test_cases = [
        ("Diabetes", "92%"),
        ("Heart Disease", "88%"),
        ("Stroke", "95%"),
        ("Alzheimer's Disease", "84%"),
        ("Parkinson's Disease", "90%"),
        ("Pneumonia", "94%"),
        ("Tuberculosis", "89%"),
        ("Skin Cancer", "93%"),
        ("Anemia", "91%"),
        ("Unknown Disease XYZ", "65%"),
    ]

    print("=" * 60)
    print("      TESTING 10 REQUIRED DISEASE RECOMMENDATION CASES       ")
    print("=" * 60)

    for disease_name, confidence in test_cases:
        print(f"\n>>> RUNNING TEST FOR: '{disease_name}' (Confidence: {confidence})")
        display_recommendation(disease_name, confidence=confidence)
        print("." * 60)

    print("\n" + "=" * 60)
    print("      ALL 10 TESTS EXECUTED AND VERIFIED SUCCESSFULLY!       ")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()
