import os
import pandas as pd
from PIL import Image

# Path to the organized datasets folder
DATASETS_DIR = r"E:\multidisease prdiction\organized_datasets"
OUTPUT_DIR = r"E:\multidisease prdiction\ML_Data_Inspection"

# Common target column name keywords
TARGET_KEYWORDS = [
    "target", "label", "class", "outcome", "diagnosis", "disease",
    "result", "status", "condition", "prediction", "classification",
    "stroke", "output", "num", "tenyearchd", "diabetes", "ckd"
]


# Function to inspect a tabular file (CSV, Data, ARFF, etc.)
def inspect_tabular_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    df = None

    try:
        if ext in [".csv", ".tsv"]:
            # Try reading with comma, then semicolon if only 1 column
            df = pd.read_csv(file_path, low_memory=False)
            if len(df.columns) == 1 and ";" in open(file_path, "r", encoding="utf-8", errors="ignore").readline():
                df = pd.read_csv(file_path, sep=";", low_memory=False)
        elif ext in [".xlsx", ".xls"]:
            df = pd.read_excel(file_path)
        elif ext in [".data", ".dat"]:
            # Common UCI whitespace or comma delimited files
            try:
                df = pd.read_csv(file_path, header=None, delim_whitespace=True, low_memory=False)
            except Exception:
                df = pd.read_csv(file_path, header=None, low_memory=False)
        elif ext == ".arff":
            # Simple line parsing for ARFF files
            data_lines = []
            col_names = []
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                reading_data = False
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("%"):
                        continue
                    if line.lower().startswith("@attribute"):
                        parts = line.split()
                        if len(parts) >= 2:
                            col_names.append(parts[1].replace("'", "").replace('"', ""))
                    elif line.lower().startswith("@data"):
                        reading_data = True
                    elif reading_data:
                        data_lines.append([v.strip() for v in line.split(",")])

            if data_lines:
                if col_names and len(col_names) == len(data_lines[0]):
                    df = pd.DataFrame(data_lines, columns=col_names)
                else:
                    df = pd.DataFrame(data_lines)
    except Exception as e:
        return None, f"Error reading file: {e}"

    if df is None or len(df) == 0:
        return None, "Empty or unsupported tabular format"

    # Gather tabular metrics
    num_rows = len(df)
    num_cols = len(df.columns)
    col_names = [str(c) for c in df.columns]
    
    # Missing values
    missing_count = int(df.isnull().sum().sum())
    
    # Check for symbol missing values like '?' or 'NA'
    for col in df.columns:
        if df[col].dtype == object:
            missing_count += int((df[col] == "?").sum())

    # Count numeric vs categorical columns
    num_numeric = len(df.select_dtypes(include=["int64", "float64", "int32", "float32"]).columns)
    num_categorical = num_cols - num_numeric

    # Duplicate rows
    num_duplicates = int(df.duplicated().sum())

    # Identify potential target column
    possible_target = "Needs Manual Review"
    num_classes = "N/A"
    class_names = "N/A"

    # 1. Search by keyword
    for col in df.columns:
        c_lower = str(col).lower().strip()
        for kw in TARGET_KEYWORDS:
            if kw == c_lower or kw in c_lower:
                possible_target = str(col)
                break
        if possible_target != "Needs Manual Review":
            break

    # 2. If not found by keyword, check the last column
    if possible_target == "Needs Manual Review" and num_cols > 1:
        last_col = df.columns[-1]
        unique_vals = df[last_col].nunique()
        # If last column has reasonable class count (e.g. <= 10)
        if unique_vals <= 10:
            possible_target = str(last_col)

    # If target is identified, get class details
    if possible_target != "Needs Manual Review" and possible_target in df.columns:
        unique_vals = df[possible_target].dropna().unique()
        num_classes = len(unique_vals)
        class_names = str(list(unique_vals)[:5])

    details = {
        "num_rows": num_rows,
        "num_cols": num_cols,
        "col_names": col_names,
        "missing_count": missing_count,
        "num_numeric": num_numeric,
        "num_categorical": num_categorical,
        "num_duplicates": num_duplicates,
        "possible_target": possible_target,
        "num_classes": num_classes,
        "class_names": class_names
    }

    return details, "Success"


# Function to inspect an image dataset directory
def inspect_image_folder(folder_path):
    image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".dcm"]
    class_counts = {}
    total_images = 0
    corrupted_images = 0
    sample_sizes = []

    for root, dirs, files in os.walk(folder_path):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in image_extensions:
                total_images += 1
                rel_dir = os.path.relpath(root, folder_path)
                class_name = rel_dir.split(os.sep)[0] if rel_dir != "." else "root"
                class_counts[class_name] = class_counts.get(class_name, 0) + 1

                img_path = os.path.join(root, f)

                # Test image integrity on sample
                if len(sample_sizes) < 5 or corrupted_images == 0:
                    try:
                        with Image.open(img_path) as img:
                            img.verify()
                        # Re-open to read dimensions
                        with Image.open(img_path) as img:
                            if len(sample_sizes) < 5:
                                sample_sizes.append(f"{img.width}x{img.height}")
                    except Exception:
                        corrupted_images += 1

    return {
        "total_images": total_images,
        "class_counts": class_counts,
        "sample_sizes": sample_sizes,
        "corrupted_images": corrupted_images
    }


# Main scanning function
def scan_and_inspect_all_datasets():
    print("=" * 60)
    print("   STEP 3: SEHATSETU DATASET INSPECTION & PREPARATION")
    print("=" * 60)
    print(f"Scanning directory: {DATASETS_DIR}\n")

    if not os.path.exists(DATASETS_DIR):
        print(f"Error: Datasets directory '{DATASETS_DIR}' not found!")
        return [], []

    report_rows = []
    text_summary_lines = []

    # Get all categories
    categories = [d for d in os.listdir(DATASETS_DIR) if os.path.isdir(os.path.join(DATASETS_DIR, d))]

    for category in categories:
        cat_path = os.path.join(DATASETS_DIR, category)
        diseases = [d for d in os.listdir(cat_path) if os.path.isdir(os.path.join(cat_path, d))]

        for disease in diseases:
            disease_path = os.path.join(cat_path, disease)
            items = os.listdir(disease_path)

            for item in items:
                item_path = os.path.join(disease_path, item)
                dataset_name = item

                # 1. Check if item is a single file in the disease folder
                if os.path.isfile(item_path):
                    ext = os.path.splitext(item)[1].lower()
                    if ext in [".csv", ".xlsx", ".xls", ".data", ".arff", ".dat"]:
                        details, msg = inspect_tabular_file(item_path)
                        if details:
                            row = {
                                "Disease": disease,
                                "Category": category,
                                "Dataset_Name": dataset_name,
                                "Dataset_Type": "Tabular",
                                "Location": item_path,
                                "Number_of_Files": 1,
                                "Number_of_Images": 0,
                                "Number_of_Rows": details["num_rows"],
                                "Number_of_Columns": details["num_cols"],
                                "Column_Names": "; ".join(details["col_names"][:10]) + ("..." if details["num_cols"] > 10 else ""),
                                "Possible_Target": details["possible_target"],
                                "Number_of_Classes": details["num_classes"],
                                "Class_Names": details["class_names"],
                                "Missing_Values": details["missing_count"],
                                "Numerical_Columns": details["num_numeric"],
                                "Categorical_Columns": details["num_categorical"],
                                "Status": "Ready for Tabular Training",
                                "Notes": f"Duplicates: {details['num_duplicates']}"
                            }
                            report_rows.append(row)

                            text_summary_lines.append(f"Disease:        {disease}")
                            text_summary_lines.append(f"Category:       {category}")
                            text_summary_lines.append(f"Dataset Name:   {dataset_name}")
                            text_summary_lines.append(f"Dataset Type:   Tabular")
                            text_summary_lines.append(f"Location:       {item_path}")
                            text_summary_lines.append(f"Rows:           {details['num_rows']}")
                            text_summary_lines.append(f"Columns:        {details['num_cols']}")
                            text_summary_lines.append(f"Target Column:  {details['possible_target']}")
                            text_summary_lines.append(f"Classes:        {details['num_classes']} ({details['class_names']})")
                            text_summary_lines.append(f"Missing Values: {details['missing_count']}")
                            text_summary_lines.append(f"Status:         Ready for Tabular Training")
                            text_summary_lines.append("-" * 50)
                    elif ext == ".zip":
                        row = {
                            "Disease": disease,
                            "Category": category,
                            "Dataset_Name": dataset_name,
                            "Dataset_Type": "Archive",
                            "Location": item_path,
                            "Number_of_Files": 1,
                            "Number_of_Images": 0,
                            "Number_of_Rows": "N/A",
                            "Number_of_Columns": "N/A",
                            "Column_Names": "N/A",
                            "Possible_Target": "N/A",
                            "Number_of_Classes": "N/A",
                            "Class_Names": "N/A",
                            "Missing_Values": "N/A",
                            "Numerical_Columns": "N/A",
                            "Categorical_Columns": "N/A",
                            "Status": "Raw Zip Archive",
                            "Notes": f"Size: {round(os.path.getsize(item_path)/(1024*1024), 2)} MB"
                        }
                        report_rows.append(row)

                # 2. Check if item is a folder
                elif os.path.isdir(item_path):
                    # List files inside
                    folder_files = []
                    for r, d, f_list in os.walk(item_path):
                        for f in f_list:
                            folder_files.append(os.path.join(r, f))

                    img_exts = [".jpg", ".jpeg", ".png", ".bmp", ".tif", ".dcm"]
                    tab_exts = [".csv", ".xlsx", ".xls", ".data", ".arff", ".dat"]

                    num_images = sum(1 for f in folder_files if os.path.splitext(f)[1].lower() in img_exts)
                    tabular_files = [f for f in folder_files if os.path.splitext(f)[1].lower() in tab_exts]

                    if num_images > len(tabular_files) and num_images > 0:
                        # Image Dataset
                        img_info = inspect_image_folder(item_path)
                        class_summary = ", ".join([f"{k}: {v}" for k, v in list(img_info["class_counts"].items())[:6]])
                        sample_size_str = ", ".join(set(img_info["sample_sizes"])) if img_info["sample_sizes"] else "N/A"

                        row = {
                            "Disease": disease,
                            "Category": category,
                            "Dataset_Name": dataset_name,
                            "Dataset_Type": "Image",
                            "Location": item_path,
                            "Number_of_Files": len(folder_files),
                            "Number_of_Images": img_info["total_images"],
                            "Number_of_Rows": "N/A",
                            "Number_of_Columns": "N/A",
                            "Column_Names": "N/A",
                            "Possible_Target": "Folder Subdirectories (Classes)",
                            "Number_of_Classes": len(img_info["class_counts"]),
                            "Class_Names": str(list(img_info["class_counts"].keys())),
                            "Missing_Values": 0,
                            "Numerical_Columns": "N/A",
                            "Categorical_Columns": "N/A",
                            "Status": "Ready for Image Training",
                            "Notes": f"Corrupted: {img_info['corrupted_images']}, Sample Dimensions: {sample_size_str}"
                        }
                        report_rows.append(row)

                        text_summary_lines.append(f"Disease:        {disease}")
                        text_summary_lines.append(f"Category:       {category}")
                        text_summary_lines.append(f"Dataset Name:   {dataset_name}")
                        text_summary_lines.append(f"Dataset Type:   Image")
                        text_summary_lines.append(f"Location:       {item_path}")
                        text_summary_lines.append(f"Total Images:   {img_info['total_images']}")
                        text_summary_lines.append(f"Classes ({len(img_info['class_counts'])}): {class_summary}")
                        text_summary_lines.append(f"Sample Sizes:   {sample_size_str}")
                        text_summary_lines.append(f"Corrupted:      {img_info['corrupted_images']}")
                        text_summary_lines.append(f"Status:         Ready for Image Training")
                        text_summary_lines.append("-" * 50)

                    elif len(tabular_files) > 0:
                        # Tabular Dataset inside folder
                        for tab_file in tabular_files:
                            file_base = os.path.basename(tab_file)
                            details, msg = inspect_tabular_file(tab_file)
                            if details:
                                row = {
                                    "Disease": disease,
                                    "Category": category,
                                    "Dataset_Name": f"{dataset_name}/{file_base}",
                                    "Dataset_Type": "Tabular",
                                    "Location": tab_file,
                                    "Number_of_Files": len(folder_files),
                                    "Number_of_Images": 0,
                                    "Number_of_Rows": details["num_rows"],
                                    "Number_of_Columns": details["num_cols"],
                                    "Column_Names": "; ".join(details["col_names"][:10]) + ("..." if details["num_cols"] > 10 else ""),
                                    "Possible_Target": details["possible_target"],
                                    "Number_of_Classes": details["num_classes"],
                                    "Class_Names": details["class_names"],
                                    "Missing_Values": details["missing_count"],
                                    "Numerical_Columns": details["num_numeric"],
                                    "Categorical_Columns": details["num_categorical"],
                                    "Status": "Ready for Tabular Training",
                                    "Notes": f"Duplicates: {details['num_duplicates']}"
                                }
                                report_rows.append(row)

                                text_summary_lines.append(f"Disease:        {disease}")
                                text_summary_lines.append(f"Category:       {category}")
                                text_summary_lines.append(f"Dataset Name:   {dataset_name}/{file_base}")
                                text_summary_lines.append(f"Dataset Type:   Tabular")
                                text_summary_lines.append(f"Location:       {tab_file}")
                                text_summary_lines.append(f"Rows:           {details['num_rows']}")
                                text_summary_lines.append(f"Columns:        {details['num_cols']}")
                                text_summary_lines.append(f"Target Column:  {details['possible_target']}")
                                text_summary_lines.append(f"Classes:        {details['num_classes']} ({details['class_names']})")
                                text_summary_lines.append(f"Missing Values: {details['missing_count']}")
                                text_summary_lines.append(f"Status:         Ready for Tabular Training")
                                text_summary_lines.append("-" * 50)

    # Save reports
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    csv_path = os.path.join(OUTPUT_DIR, "dataset_report.csv")
    txt_path = os.path.join(OUTPUT_DIR, "dataset_report.txt")

    df_report = pd.DataFrame(report_rows)
    df_report.to_csv(csv_path, index=False)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("======================================================================\n")
        f.write("           SEHATSETU - DATASET INSPECTION REPORT                      \n")
        f.write("======================================================================\n\n")
        f.write("\n".join(text_summary_lines))
        f.write("\n\n======================================================================\n")
        f.write(f"Total Datasets/Files Inspected: {len(report_rows)}\n")
        f.write("======================================================================\n")

    print("\n" + "=" * 60)
    print(f"Inspection complete! Generated reports at:")
    print(f"  1. {csv_path}")
    print(f"  2. {txt_path}")
    print("=" * 60)

    return report_rows, text_summary_lines


if __name__ == "__main__":
    scan_and_inspect_all_datasets()
