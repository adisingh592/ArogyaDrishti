@echo off
cd /d "%~dp0"
echo ======================================================================
echo           SEHATSETU - RUNNING DATASET INSPECTION
echo ======================================================================
echo.
python inspect_datasets.py
echo.
echo ======================================================================
echo Inspection finished! Check dataset_report.csv and dataset_report.txt.
echo ======================================================================
pause
