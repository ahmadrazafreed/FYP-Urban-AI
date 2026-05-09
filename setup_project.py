"""
FYP - AI-Driven Sustainable Urban Management System
Run this file ONCE to set up your entire project structure
"""

import os

# ── Folder structure ──────────────────────────────────────────
folders = [
    "FYP_UrbanManagement/data/raw",
    "FYP_UrbanManagement/data/processed",
    "FYP_UrbanManagement/models",
    "FYP_UrbanManagement/notebooks",
    "FYP_UrbanManagement/app",
    "FYP_UrbanManagement/database",
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"✅ Created: {folder}")

# ── requirements.txt ──────────────────────────────────────────
requirements = """pandas
numpy
scikit-learn
matplotlib
seaborn
streamlit
joblib
sqlalchemy
"""

with open("FYP_UrbanManagement/requirements.txt", "w") as f:
    f.write(requirements)
print("✅ Created: requirements.txt")

print("\n" + "="*50)
print("PROJECT SETUP COMPLETE!")
print("="*50)
print("\nNext step — open your terminal and run:")
print("  cd FYP_UrbanManagement")
print("  pip install -r requirements.txt")
