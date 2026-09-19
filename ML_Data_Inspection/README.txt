======================================================================
           SEHATSETU - DATASET INSPECTION MODULE (STEP 3)
======================================================================

1. PURPOSE
----------
This module is responsible for scanning and inspecting all organized medical
datasets located at:
E:\multidisease prdiction\organized_datasets

It performs a 100% read-only diagnostic inspection to determine:
* Modality (Tabular vs Image vs EEG/Time-Series vs Text/Archive)
* Row, column, and file counts
* Column names and data types (numeric vs categorical)
* Missing values and duplicate records
* Detection of potential target / label columns and unique class counts
* Image dataset folder-class structures, sample image resolutions, and file integrity


2. FILES IN THIS FOLDER
-----------------------
* inspect_datasets.py   : Main Python inspection script.
* inspect_datasets.bat  : Windows batch file to run inspection in one click.
* dataset_report.csv    : Structured CSV report of all inspected datasets.
* dataset_report.txt    : Clean, human-readable summary of all inspected datasets.
* README.txt            : This documentation file.


3. HOW TO RUN
-------------
Option A (Command Prompt / VS Code Terminal):
   cd "ML_Data_Inspection"
   python inspect_datasets.py

Option B (Double Click Batch File):
   Double-click `inspect_datasets.bat`


4. SAFETY & NON-DESTRUCTIVE GUARANTEE
-------------------------------------
* This tool NEVER modifies, resizes, converts, moves, or deletes any dataset files.
* All data is read in read-only mode for analysis and report generation.
======================================================================
