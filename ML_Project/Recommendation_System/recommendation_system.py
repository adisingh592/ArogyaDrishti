import json
import os

# Set the confidence threshold (can be changed easily)
CONFIDENCE_THRESHOLD = 70.0


# Function to load disease data from JSON file
def load_knowledge_base():
    # Find the path of the json file in the same folder as this script
    current_folder = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_folder, "disease_information.json")

    try:
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get("diseases", {})
    except Exception as e:
        print(f"Error loading disease_information.json: {e}")
        return {}


# Function to clean and simplify disease name for easy matching
def clean_disease_name(name):
    clean_name = name.lower().strip()
    clean_name = clean_name.replace("'", "")
    clean_name = clean_name.replace("-", " ")
    clean_name = clean_name.replace("_", " ")
    return clean_name


# Main function to get recommendation for a disease
def get_recommendation(disease_name):
    # Load all disease data
    diseases_data = load_knowledge_base()

    if not diseases_data:
        return None

    user_clean_name = clean_disease_name(disease_name)

    # 1. First try exact key match
    for key in diseases_data:
        if clean_disease_name(key) == user_clean_name:
            return diseases_data[key]

    # 2. Try partial matching for common student inputs (e.g. 'alzheimer', 'parkinson', 'tb', 'kidney')
    for key, info in diseases_data.items():
        db_clean_name = clean_disease_name(key)

        if user_clean_name in db_clean_name or db_clean_name in user_clean_name:
            return info

        # Handle specific common abbreviations
        if user_clean_name == "tb" and "tuberculosis" in db_clean_name:
            return info
        if user_clean_name == "ckd" and "kidney" in db_clean_name:
            return info
        if user_clean_name == "covid" and "covid" in db_clean_name:
            return info

    # If disease is not found
    return None


# Function to display the formatted recommendation output
def display_recommendation(disease_name, confidence=None, category=None):
    # Retrieve the disease details from json
    info = get_recommendation(disease_name)

    # If the disease is not in our knowledge base
    if info is None:
        print("\n" + "=" * 40)
        print("No information is available for this disease.")
        print("\nPlease consult a qualified healthcare professional")
        print("for appropriate information.")
        print("=" * 40 + "\n")
        return

    # Use category from JSON if not provided
    display_category = category if category else info.get("category", "General")

    print("\n" + "=" * 40)
    print("HEALTH RECOMMENDATION")
    print("=" * 40)

    print(f"\nDisease:\n{disease_name.title()}")

    # Display confidence if passed from ML model
    if confidence is not None:
        conf_str = str(confidence).strip()
        if not conf_str.endswith("%"):
            conf_str = conf_str + "%"
        print(f"\nPrediction Confidence:\n{conf_str}")

        # Check if prediction confidence is low
        try:
            num_conf = float(conf_str.replace("%", ""))
            if num_conf < CONFIDENCE_THRESHOLD:
                print("\n" + "-" * 40)
                print("WARNING:")
                print("The prediction confidence is low.")
                print("This result should not be relied upon for medical decisions.")
                print("Professional medical evaluation is recommended.")
                print("-" * 40)
        except Exception:
            pass

    print(f"\nCategory:\n{display_category}")

    # Display dataset availability in project
    dataset_info = info.get("dataset_info", {})
    print("\n" + "-" * 40)
    print("DATASET IN PROJECT")
    print("-" * 40)
    if dataset_info.get("is_dataset_present", False):
        print(f"Status:   Dataset Available in Project")
        print(f"Dataset:  {dataset_info.get('dataset_name', 'N/A')}")
        print(f"Type:     {dataset_info.get('data_type', 'N/A')}")
        print(f"Location: {dataset_info.get('folder_path', 'N/A')}")
    else:
        print("Status:   Reference Condition (No local dataset in project)")

    # 1. Description
    print("\n" + "-" * 40)
    print("DESCRIPTION")
    print("-" * 40)
    print(info.get("description", "Information not available."))

    # 2. Common Types (if available)
    common_types = info.get("common_types", [])
    if common_types:
        print("\n" + "-" * 40)
        print("COMMON TYPES")
        print("-" * 40)
        for item in common_types:
            print(f"* {item}")

    # 3. Symptoms
    print("\n" + "-" * 40)
    print("COMMON SYMPTOMS")
    print("-" * 40)
    for symptom in info.get("symptoms", []):
        print(f"* {symptom}")

    # 4. Risk Factors
    print("\n" + "-" * 40)
    print("RISK FACTORS")
    print("-" * 40)
    for risk in info.get("risk_factors", []):
        print(f"* {risk}")

    # 5. Food Recommendations
    food_data = info.get("food", {})
    print("\n" + "-" * 40)
    print("FOOD RECOMMENDATIONS")
    print("-" * 40)

    print("\nFoods to Prefer:")
    for food in food_data.get("prefer", []):
        print(f"* {food}")

    print("\nFoods to Limit:")
    for food in food_data.get("limit", []):
        print(f"* {food}")

    general_food_tip = food_data.get("general_tip", "")
    if general_food_tip:
        print(f"\nGeneral Healthy Eating Tip:\n{general_food_tip}")

    # 6. Exercise Recommendations
    exercise_data = info.get("exercise", {})
    print("\n" + "-" * 40)
    print("EXERCISE RECOMMENDATIONS")
    print("-" * 40)

    print("\nRecommended Activities:")
    for ex in exercise_data.get("recommended", []):
        print(f"* {ex}")

    print("\nExercise Precautions:")
    for precaution in exercise_data.get("precautions", []):
        print(f"* {precaution}")

    print("\nNote: Exercise recommendations should be adjusted according to individual health status and ability.")

    # 7. Lifestyle
    print("\n" + "-" * 40)
    print("LIFESTYLE RECOMMENDATIONS")
    print("-" * 40)
    for life in info.get("lifestyle", []):
        print(f"* {life}")

    # 8. Monitoring
    print("\n" + "-" * 40)
    print("GENERAL MONITORING INFORMATION")
    print("-" * 40)
    for mon in info.get("monitoring", []):
        print(f"* {mon}")

    # 9. Medical Guidance
    print("\n" + "-" * 40)
    print("GENERAL MEDICAL GUIDANCE")
    print("-" * 40)
    for guide in info.get("medical_guidance", []):
        print(f"* {guide}")

    # 10. Warning Signs
    print("\n" + "-" * 40)
    print("WARNING SIGNS")
    print("-" * 40)
    for warn in info.get("warning_signs", []):
        print(f"* {warn}")

    # 11. When to Seek Help
    print("\n" + "-" * 40)
    print("WHEN TO SEEK PROFESSIONAL MEDICAL HELP")
    print("-" * 40)
    for help_case in info.get("when_to_seek_help", []):
        print(f"* {help_case}")

    # 12. Reliable Information Sources
    print("\n" + "-" * 40)
    print("RELIABLE INFORMATION SOURCES")
    print("-" * 40)
    for src in info.get("sources", []):
        print(f"* {src}")

    # 13. Emergency Notice
    print("\n" + "-" * 40)
    print("IMPORTANT EMERGENCY NOTICE")
    print("-" * 40)
    print("Some symptoms may require urgent medical attention.")
    print("If severe or rapidly worsening symptoms occur,")
    print("seek immediate professional medical care or contact")
    print("your local emergency medical service.")

    # 14. Educational Disclaimer
    print("\n" + "-" * 40)
    print("DISCLAIMER")
    print("-" * 40)
    print("This system provides general educational health information only.")
    print("It is not a substitute for professional medical diagnosis,")
    print("treatment, or individualized medical advice.")
    print("\nDo not start, stop, or change medication based on this system.")
    print("Consult a qualified healthcare professional for personal medical advice.")
    print("=" * 40 + "\n")


# Interactive Mode (When run directly by user)
if __name__ == "__main__":
    print("==================================================")
    print("   MULTI-DISEASE HEALTH RECOMMENDATION SYSTEM     ")
    print("==================================================")

    # Ask user for disease name
    user_disease = input("Enter detected disease: ").strip()

    # Ask optionally for confidence (or leave empty)
    user_conf = input("Enter prediction confidence (optional, e.g. 91%): ").strip()

    if user_disease:
        if user_conf:
            display_recommendation(user_disease, confidence=user_conf)
        else:
            display_recommendation(user_disease)
    else:
        print("Please enter a valid disease name.")
