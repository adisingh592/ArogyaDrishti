==================================================
SEHATSETU - HEALTH RECOMMENDATION SUBSYSTEM
==================================================

1. Overview:
   A deterministic, rule-based clinical recommendation engine powered by structured knowledge base (disease_information.json).
   Provides safe lifestyle, dietary, exercise, monitoring, and medical consultation guidance.

2. Safety Guidelines (Strict Medical Disclaimer):
   - DOES NOT prescribe medicines or dosages.
   - DOES NOT instruct patients to start or stop medications.
   - DOES NOT claim diets or foods cure diseases.
   - Emphasizes professional healthcare consultation.

3. Files:
   - recommendation_system.py: Main recommendation logic, CLI query interface, and display formatter.
   - disease_information.json: Structured knowledge base covering 34+ medical conditions across 13 clinical dimensions.
   - test_recommendation_system.py: Test suite verifying disease queries and low-confidence warning triggers.

4. Usage:
   From Python:
   from recommendation_system import display_recommendation
   display_recommendation("Diabetes", confidence="92%")
