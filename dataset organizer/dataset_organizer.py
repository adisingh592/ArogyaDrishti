import os
import shutil


# Function to identify disease name from folder or file name
def identify_disease(name):
    name = name.lower()

    if "diabetes" in name or "diabetic" in name:
        return "Diabetes"
    elif "stroke" in name:
        return "Stroke"
    elif "heart" in name or "cardio" in name or "statlog" in name:
        return "Heart_Disease"
    elif "kidney" in name or "ckd" in name:
        return "Chronic_Kidney_Disease"
    elif "liver" in name or "ilpd" in name:
        return "Liver_Disease"
    elif "breast" in name:
        return "Breast_Cancer"
    elif "cervical" in name or "cencer" in name:
        return "Cervical_Cancer"
    elif "luekemina" in name or "leukemia" in name:
        return "Leukemia"
    elif "skin" in name or "melanoma" in name or "ham10000" in name:
        return "Skin_Cancer"
    elif "brain" in name or "tumour" in name or "tumor" in name:
        return "Brain_Tumor"
    elif "alzheimer" in name or "alhezhimer" in name:
        return "Alzheimers_Disease"
    elif "anemia" in name:
        return "Anemia"
    elif "obesity" in name or "eating" in name:
        return "Obesity_and_Lifestyle"
    elif "maternal" in name:
        return "Maternal_Health_Risk"
    elif "tb" in name or "tuberculosis" in name or "chest" in name:
        return "Tuberculosis"
    elif "malaria" in name:
        return "Malaria"
    elif "thyroid" in name or "hypo" in name:
        return "Thyroid_Disease"
    elif "pneumonia" in name:
        return "Pneumonia"
    elif "covid" in name:
        return "COVID_19"
    else:
        return "Other_Diseases"


# Function to identify category based on disease
def identify_category(disease):
    if disease in ["Diabetes", "Thyroid_Disease", "Obesity_and_Lifestyle"]:
        return "Endocrine_Metabolic"
    elif disease in ["Heart_Disease", "Stroke"]:
        return "Cardiovascular"
    elif disease in ["Chronic_Kidney_Disease"]:
        return "Renal_System"
    elif disease in ["Liver_Disease"]:
        return "Hepatic_System"
    elif disease in ["Tuberculosis", "Pneumonia", "COVID_19"]:
        return "Respiratory"
    elif disease in ["Brain_Tumor", "Alzheimers_Disease"]:
        return "Neurological"
    elif disease in ["Breast_Cancer", "Cervical_Cancer", "Skin_Cancer"]:
        return "Oncology_Dermatology"
    elif disease in ["Anemia", "Leukemia"]:
        return "Hematology"
    elif disease in ["Malaria"]:
        return "Infectious_Diseases"
    elif disease in ["Maternal_Health_Risk"]:
        return "Obstetrics_Gynecology"
    else:
        return "General_Diseases"


# Function to organize all datasets into category and disease folders
def organize_all_datasets(source_directory, target_directory):
    print("==================================================")
    print("      ORGANIZING MULTI-DISEASE DATASETS           ")
    print("==================================================")
    print(f"Source Folder:      {source_directory}")
    print(f"Destination Folder: {target_directory}\n")

    # Check if source exists
    if not os.path.exists(source_directory):
        print(f"Source path '{source_directory}' does not exist!")
        return

    # Create destination folder if not exists
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    # Get all items in source directory
    all_items = os.listdir(source_directory)

    total_items = len(all_items)
    processed_count = 0

    # Loop through each item in the source folder
    for item in all_items:
        source_path = os.path.join(source_directory, item)

        # Decide disease and category
        disease = identify_disease(item)
        category = identify_category(disease)

        # Build target folder path: organized_datasets / Category / Disease
        destination_folder = os.path.join(target_directory, category, disease)

        # Create destination folder if not exists
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        # If it is a directory/folder
        if os.path.isdir(source_path):
            target_path = os.path.join(destination_folder, item)
            
            print(f"[{processed_count + 1}/{total_items}] Copying folder: '{item}'")
            print(f"   --> Target: {category} / {disease} / {item}")

            # Copy folder contents
            if not os.path.exists(target_path):
                shutil.copytree(source_path, target_path)
                print("   [Done]")
            else:
                print("   [Already exists, skipped]")

        # If it is a single file (like zip or csv)
        elif os.path.isfile(source_path):
            target_path = os.path.join(destination_folder, item)

            print(f"[{processed_count + 1}/{total_items}] Copying file: '{item}'")
            print(f"   --> Target: {category} / {disease} / {item}")

            # Copy file
            if not os.path.exists(target_path):
                shutil.copy2(source_path, target_path)
                print("   [Done]")
            else:
                print("   [Already exists, skipped]")

        processed_count += 1
        print("-" * 50)

    print("\nAll datasets have been successfully organized into folders!")


# Main Program
if __name__ == "__main__":
    # Source dataset path
    SOURCE_PATH = r"E:\Ml project"

    # Destination folder where all organized datasets will be placed
    TARGET_PATH = r"E:\multidisease prdiction\organized_datasets"

    # Remove previous report file if present
    report_file = r"E:\multidisease prdiction\dataset_report.csv"
    if os.path.exists(report_file):
        os.remove(report_file)

    # Run the organizer
    organize_all_datasets(SOURCE_PATH, TARGET_PATH)
