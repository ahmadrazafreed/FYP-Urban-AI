"""
FYP - AI-Driven Urban Management System
MODULE 1 (IMPROVED): Flood Prediction Model
- Uses Gradient Boosting for better accuracy
- Adds feature engineering to boost R² score
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os

print("=" * 55)
print("  FYP - Flood Prediction Model (Improved)")
print("=" * 55)

# ── STEP 1: Load Data ─────────────────────────────────────────
df = pd.read_csv("data/raw/flood.csv")
print(f"✅ Loaded flood.csv — {len(df):,} rows")

if 'id' in df.columns:
    df = df.drop(columns=['id'])

df = df.fillna(df.median(numeric_only=True))
df = df[(df['FloodProbability'] >= 0) & (df['FloodProbability'] <= 1)]

# ── STEP 2: Feature Engineering (NEW!) ───────────────────────
print("\n── Adding Engineered Features ────────────────────────")

# Combine related features into meaningful groups
df['Infrastructure_Risk'] = (
    df['DeterioratingInfrastructure'] +
    df['DrainageSystems'] +
    df['DamsQuality']
) / 3

df['Human_Activity_Risk'] = (
    df['Deforestation'] +
    df['Urbanization'] +
    df['AgriculturalPractices'] +
    df['Encroachments']
) / 4

df['Climate_Risk'] = (
    df['MonsoonIntensity'] +
    df['ClimateChange'] +
    df['WetlandLoss']
) / 3

df['Governance_Risk'] = (
    df['IneffectiveDisasterPreparedness'] +
    df['InadequatePlanning'] +
    df['PoliticalFactors']
) / 3

df['Total_Risk_Score'] = (
    df['Infrastructure_Risk'] +
    df['Human_Activity_Risk'] +
    df['Climate_Risk'] +
    df['Governance_Risk']
)

print("✅ Added 5 engineered features")

# ── STEP 3: Prepare Features ──────────────────────────────────
FEATURES = [
    'MonsoonIntensity', 'TopographyDrainage', 'RiverManagement',
    'Deforestation', 'Urbanization', 'ClimateChange', 'DamsQuality',
    'Siltation', 'AgriculturalPractices', 'Encroachments',
    'IneffectiveDisasterPreparedness', 'DrainageSystems',
    'CoastalVulnerability', 'Landslides', 'Watersheds',
    'DeterioratingInfrastructure', 'PopulationScore', 'WetlandLoss',
    'InadequatePlanning', 'PoliticalFactors',
    # Engineered features
    'Infrastructure_Risk', 'Human_Activity_Risk',
    'Climate_Risk', 'Governance_Risk', 'Total_Risk_Score'
]
TARGET = 'FloodProbability'

X = df[FEATURES]
y = df[TARGET]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"✅ Train: {len(X_train):,} | Test: {len(X_test):,}")

# ── STEP 4: Train Gradient Boosting Model ─────────────────────
print("\n── Training Gradient Boosting Model ──────────────────")
print("   Please wait ~2 minutes...")

model = GradientBoostingRegressor(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=5,
    random_state=42
)
model.fit(X_train, y_train)
print("✅ Model trained!")

# ── STEP 5: Evaluate ──────────────────────────────────────────
print("\n── Model Evaluation ──────────────────────────────────")
y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
r2  = r2_score(y_test, y_pred)

print(f"✅ MAE (Mean Absolute Error) : {mae:.4f}")
print(f"✅ R² Score                  : {r2:.4f}")

# ── STEP 6: Feature Importance ────────────────────────────────
print("\n── Top 5 Most Important Factors ──────────────────────")
importance_df = pd.DataFrame({
    'Feature': FEATURES,
    'Importance': model.feature_importances_
}).sort_values('Importance', ascending=False)
print(importance_df.head(5).to_string(index=False))

# ── STEP 7: Save ──────────────────────────────────────────────
print("\n── Saving Files ──────────────────────────────────────")
os.makedirs("models", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)

joblib.dump(model,    "models/flood_model.pkl")
joblib.dump(FEATURES, "models/flood_features.pkl")
df.to_csv("data/processed/flood_clean.csv", index=False)

print("✅ Model saved    : models/flood_model.pkl")
print("✅ Features saved : models/flood_features.pkl")
print("✅ Clean data     : data/processed/flood_clean.csv")

# ── STEP 8: Plot ──────────────────────────────────────────────
plt.figure(figsize=(10, 7))
sns.barplot(data=importance_df, x='Importance', y='Feature', palette='Blues_r')
plt.title('Flood Prediction - Feature Importance (Improved Model)', fontsize=13)
plt.xlabel('Importance Score')
plt.tight_layout()
plt.savefig("data/processed/flood_feature_importance.png", dpi=150)
plt.show()
print("✅ Chart saved    : data/processed/flood_feature_importance.png")

print("\n" + "=" * 55)
print("  MODULE 1 COMPLETE! ✅")
print(f"  Final R² Score: {r2:.4f}")
print("  Next step: Run generate_waste_dataset.py")
print("           then waste_model.py")
print("=" * 55)
