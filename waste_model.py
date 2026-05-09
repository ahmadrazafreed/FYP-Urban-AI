"""
FYP - AI-Driven Urban Management System
MODULE 2: Smart Waste Management Model
- Predicts if a bin needs collection
- Predicts fill level at next reading
- Saves model for dashboard
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, classification_report, r2_score, mean_absolute_error
import joblib
import os

print("=" * 55)
print("  FYP - Smart Waste Management Model")
print("=" * 55)

# ── STEP 1: Load Data ─────────────────────────────────────────
df = pd.read_csv("data/raw/smart_waste_data.csv")
print(f"✅ Loaded smart_waste_data.csv — {len(df):,} rows")
print(f"   Columns: {list(df.columns)}")

# ── STEP 2: Feature Engineering ───────────────────────────────
print("\n── Engineering Features ──────────────────────────────")

# Convert timestamp to useful features
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['hour']       = df['timestamp'].dt.hour
df['day_of_week'] = df['timestamp'].dt.dayofweek   # 0=Monday
df['month']      = df['timestamp'].dt.month

# Previous fill level per bin (shift by 1 reading)
df = df.sort_values(['bin_id', 'timestamp'])
df['prev_fill_level'] = df.groupby('bin_id')['fill_level_%'].shift(1)
df['fill_change']     = df['fill_level_%'] - df['prev_fill_level']

# Encode bin_type as numbers
df['bin_type_code'] = df['bin_type'].map({
    'General': 0, 'Recyclable': 1, 'Organic': 2
})

# Drop rows where prev_fill_level is NaN (first reading per bin)
df = df.dropna(subset=['prev_fill_level'])
print(f"✅ After feature engineering: {len(df):,} rows")

# ── STEP 3: Define Features ───────────────────────────────────
FEATURES = [
    'prev_fill_level',
    'fill_change',
    'hour',
    'day_of_week',
    'month',
    'is_weekend',
    'temperature_C',
    'humidity_%',
    'bin_type_code',
]
TARGET_CLASS = 'collection_needed'   # 0 or 1
TARGET_REG   = 'fill_level_%'        # actual fill %

X = df[FEATURES]
y_class = df[TARGET_CLASS]
y_reg   = df[TARGET_REG]

# ── STEP 4: Train/Test Split ──────────────────────────────────
X_train, X_test, yc_train, yc_test, yr_train, yr_test = train_test_split(
    X, y_class, y_reg, test_size=0.2, random_state=42
)
print(f"\n✅ Train: {len(X_train):,} | Test: {len(X_test):,}")

# ── STEP 5A: Classification Model (needs collection?) ─────────
print("\n── Training Classifier (collection needed?) ──────────")
clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
clf.fit(X_train, yc_train)

yc_pred = clf.predict(X_test)
acc = accuracy_score(yc_test, yc_pred)
print(f"✅ Accuracy: {acc:.4f} ({acc*100:.1f}%)")
print("\nClassification Report:")
print(classification_report(yc_test, yc_pred, target_names=['No Collection', 'Needs Collection']))

# ── STEP 5B: Regression Model (predict fill level) ────────────
print("\n── Training Regressor (fill level prediction) ────────")
reg = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
reg.fit(X_train, yr_train)

yr_pred = reg.predict(X_test)
mae = mean_absolute_error(yr_test, yr_pred)
r2  = r2_score(yr_test, yr_pred)
print(f"✅ MAE      : {mae:.4f}%")
print(f"✅ R² Score : {r2:.4f}")

# ── STEP 6: Feature Importance ────────────────────────────────
print("\n── Top 5 Most Important Features ─────────────────────")
imp_df = pd.DataFrame({
    'Feature': FEATURES,
    'Importance': clf.feature_importances_
}).sort_values('Importance', ascending=False)
print(imp_df.head(5).to_string(index=False))

# ── STEP 7: Save Everything ───────────────────────────────────
print("\n── Saving Files ──────────────────────────────────────")
os.makedirs("models", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)

joblib.dump(clf,      "models/waste_classifier.pkl")
joblib.dump(reg,      "models/waste_regressor.pkl")
joblib.dump(FEATURES, "models/waste_features.pkl")
df.to_csv("data/processed/waste_clean.csv", index=False)

print("✅ Classifier saved  : models/waste_classifier.pkl")
print("✅ Regressor saved   : models/waste_regressor.pkl")
print("✅ Features saved    : models/waste_features.pkl")
print("✅ Clean data saved  : data/processed/waste_clean.csv")

# ── STEP 8: Quick Visualizations ──────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Chart 1: Feature importance
sns.barplot(data=imp_df, x='Importance', y='Feature', palette='Oranges_r', ax=axes[0])
axes[0].set_title('Feature Importance — Collection Prediction')
axes[0].set_xlabel('Importance Score')

# Chart 2: Fill level by bin type
avg_fill = df.groupby(['area', 'bin_type'])['fill_level_%'].mean().reset_index()
sns.barplot(data=df, x='bin_type', y='fill_level_%', palette='Set2', ax=axes[1])
axes[1].set_title('Average Fill Level by Bin Type')
axes[1].set_xlabel('Bin Type')
axes[1].set_ylabel('Average Fill Level (%)')

plt.tight_layout()
plt.savefig("data/processed/waste_analysis.png", dpi=150)
plt.show()
print("✅ Chart saved : data/processed/waste_analysis.png")

# ── STEP 9: Test a Live Prediction ───────────────────────────
print("\n── Live Prediction Test ──────────────────────────────")
sample = pd.DataFrame([{
    'prev_fill_level': 72.0,
    'fill_change':      8.5,
    'hour':            14,
    'day_of_week':      5,    # Saturday
    'month':            3,
    'is_weekend':       1,
    'temperature_C':   38.0,
    'humidity_%':      75.0,
    'bin_type_code':    0,    # General
}])

pred_class = clf.predict(sample)[0]
pred_fill  = reg.predict(sample)[0]
print(f"   Input  : 72% full, Saturday, 38°C, General bin")
print(f"   Output : Collection needed = {'YES ⚠️' if pred_class == 1 else 'NO ✅'}")
print(f"   Output : Predicted next fill level = {pred_fill:.1f}%")

print("\n" + "=" * 55)
print("  MODULE 2 COMPLETE! ✅")
print("  Both models trained and saved!")
print("  Next step: Build the Streamlit dashboard")
print("=" * 55)
