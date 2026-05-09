"""
FYP - Smart Waste Management Dataset Generator
Run this script to generate a realistic smart bin sensor dataset.
Output: data/raw/smart_waste_data.csv
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

# Seed for reproducibility
np.random.seed(42)

# ── Settings ──────────────────────────────────────────────────
NUM_BINS   = 10
DAYS       = 90          # 3 months of data
READS_PER_DAY = 6        # sensor reads every 4 hours

# ── Bin locations (Karachi areas for realism) ─────────────────
bins = [
    {"bin_id": "BIN_001", "area": "Saddar",        "bin_type": "General",    "lat": 24.8607, "lon": 67.0105},
    {"bin_id": "BIN_002", "area": "Clifton",        "bin_type": "Recyclable", "lat": 24.8138, "lon": 67.0300},
    {"bin_id": "BIN_003", "area": "Gulshan",        "bin_type": "General",    "lat": 24.9215, "lon": 67.0977},
    {"bin_id": "BIN_004", "area": "North Nazimabad","bin_type": "Organic",    "lat": 24.9480, "lon": 67.0630},
    {"bin_id": "BIN_005", "area": "Korangi",        "bin_type": "General",    "lat": 24.8300, "lon": 67.1300},
    {"bin_id": "BIN_006", "area": "Malir",          "bin_type": "Recyclable", "lat": 24.8930, "lon": 67.2060},
    {"bin_id": "BIN_007", "area": "Lyari",          "bin_type": "Organic",    "lat": 24.8558, "lon": 66.9922},
    {"bin_id": "BIN_008", "area": "DHA",            "bin_type": "General",    "lat": 24.7925, "lon": 67.0601},
    {"bin_id": "BIN_009", "area": "Landhi",         "bin_type": "Recyclable", "lat": 24.8560, "lon": 67.1900},
    {"bin_id": "BIN_010", "area": "PECHS",          "bin_type": "Organic",    "lat": 24.8720, "lon": 67.0610},
]

# ── Fill rate per bin type (how fast they fill up) ────────────
fill_rates = {
    "General":    np.random.uniform(8, 15),   # fills faster
    "Recyclable": np.random.uniform(4, 9),
    "Organic":    np.random.uniform(6, 12),
}

# ── Generate data ─────────────────────────────────────────────
records = []
start_date = datetime(2024, 1, 1)

for bin_info in bins:
    fill_level = np.random.uniform(0, 20)  # start with some waste
    base_fill_rate = fill_rates[bin_info["bin_type"]]

    for day in range(DAYS):
        current_date = start_date + timedelta(days=day)
        is_weekend = current_date.weekday() >= 5

        for reading in range(READS_PER_DAY):
            timestamp = current_date + timedelta(hours=reading * 4)

            # Weekends fill faster (more activity)
            daily_rate = base_fill_rate * (1.3 if is_weekend else 1.0)
            # Add some random noise
            noise = np.random.normal(0, 1.5)
            fill_level += (daily_rate / READS_PER_DAY) + noise
            fill_level = np.clip(fill_level, 0, 100)

            # Bin gets collected when it hits 85%+
            collected = False
            if fill_level >= 85:
                collected = True

            # Temperature & humidity (affects organic waste)
            temperature = np.random.uniform(28, 42)   # Karachi temps
            humidity    = np.random.uniform(55, 90)

            records.append({
                "timestamp":        timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "bin_id":           bin_info["bin_id"],
                "area":             bin_info["area"],
                "bin_type":         bin_info["bin_type"],
                "latitude":         bin_info["lat"],
                "longitude":        bin_info["lon"],
                "fill_level_%":     round(fill_level, 2),
                "temperature_C":    round(temperature, 1),
                "humidity_%":       round(humidity, 1),
                "is_weekend":       int(is_weekend),
                "collection_needed": int(fill_level >= 75),
                "collected":        int(collected),
            })

            # Reset after collection
            if collected:
                fill_level = np.random.uniform(0, 10)

# ── Save to CSV ───────────────────────────────────────────────
os.makedirs("FYP_UrbanManagement/data/raw", exist_ok=True)
df = pd.DataFrame(records)
output_path = "FYP_UrbanManagement/data/raw/smart_waste_data.csv"
df.to_csv(output_path, index=False)

# ── Summary ───────────────────────────────────────────────────
print("=" * 50)
print("✅ DATASET GENERATED SUCCESSFULLY!")
print("=" * 50)
print(f"📁 Saved to   : {output_path}")
print(f"📊 Total rows : {len(df):,}")
print(f"🗑️  Bins       : {NUM_BINS}")
print(f"📅 Days       : {DAYS} (Jan–Mar 2024)")
print(f"📍 Areas      : Karachi locations")
print("\n── Column Overview ──────────────────────────")
print(df.dtypes.to_string())
print("\n── Sample (first 3 rows) ────────────────────")
print(df.head(3).to_string(index=False))
print("\n── Fill Level Stats ─────────────────────────")
print(df["fill_level_%"].describe().round(2))
