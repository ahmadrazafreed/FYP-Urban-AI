"""
FYP - Auto Model Setup
Run this ONCE before deploying to Streamlit Cloud.
It trains both models and saves them to the models/ folder.
You then push the models/ folder to GitHub.

Run: python setup_models.py
"""

import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor, RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, accuracy_score

print("=" * 55)
print("  FYP — Auto Model Setup for Deployment")
print("=" * 55)

os.makedirs("models", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)

# ── CHECK if models already exist ────────────────────────────
models_exist = all(os.path.exists(f"models/{f}") for f in [
    "flood_model.pkl","flood_features.pkl",
    "waste_classifier.pkl","waste_regressor.pkl","waste_features.pkl"
])

if models_exist:
    print("✅ All models already exist — no retraining needed!")
    print("   You can push to GitHub directly.")
else:
    print("⚠️  Some models missing — training now...")

# ── FLOOD MODEL ───────────────────────────────────────────────
if not os.path.exists("models/flood_model.pkl"):
    print("\n── Training Flood Model ──────────────────────────────")
    if os.path.exists("data/raw/flood.csv"):
        df = pd.read_csv("data/raw/flood.csv")
    elif os.path.exists("data/raw/train.csv"):
        df = pd.read_csv("data/raw/train.csv").sample(50000, random_state=42)
    else:
        print("❌ ERROR: No flood dataset found in data/raw/")
        print("   Please put flood.csv in data/raw/ and run again.")
        exit(1)

    if 'id' in df.columns: df = df.drop(columns=['id'])
    df = df.fillna(df.median(numeric_only=True))
    df = df[(df['FloodProbability']>=0)&(df['FloodProbability']<=1)]

    df['Infrastructure_Risk'] = (df['DeterioratingInfrastructure']+df['DrainageSystems']+df['DamsQuality'])/3
    df['Human_Activity_Risk'] = (df['Deforestation']+df['Urbanization']+df['AgriculturalPractices']+df['Encroachments'])/4
    df['Climate_Risk']        = (df['MonsoonIntensity']+df['ClimateChange']+df['WetlandLoss'])/3
    df['Governance_Risk']     = (df['IneffectiveDisasterPreparedness']+df['InadequatePlanning']+df['PoliticalFactors'])/3
    df['Total_Risk_Score']    = df['Infrastructure_Risk']+df['Human_Activity_Risk']+df['Climate_Risk']+df['Governance_Risk']

    FEATURES = [
        'MonsoonIntensity','TopographyDrainage','RiverManagement','Deforestation',
        'Urbanization','ClimateChange','DamsQuality','Siltation','AgriculturalPractices',
        'Encroachments','IneffectiveDisasterPreparedness','DrainageSystems',
        'CoastalVulnerability','Landslides','Watersheds','DeterioratingInfrastructure',
        'PopulationScore','WetlandLoss','InadequatePlanning','PoliticalFactors',
        'Infrastructure_Risk','Human_Activity_Risk','Climate_Risk','Governance_Risk','Total_Risk_Score'
    ]

    X = df[FEATURES]; y = df['FloodProbability']
    Xtr,Xte,ytr,yte = train_test_split(X,y,test_size=.2,random_state=42)

    model = GradientBoostingRegressor(n_estimators=200,learning_rate=.05,max_depth=5,random_state=42)
    model.fit(Xtr,ytr)
    r2  = r2_score(yte, model.predict(Xte))
    mae = mean_absolute_error(yte, model.predict(Xte))
    print(f"✅ Flood Model — R²: {r2:.4f} | MAE: {mae:.4f}")

    joblib.dump(model,    "models/flood_model.pkl")
    joblib.dump(FEATURES, "models/flood_features.pkl")
    df.to_csv("data/processed/flood_clean.csv", index=False)
    print("✅ Saved: models/flood_model.pkl")
else:
    print("✅ Flood model already exists — skipping")

# ── WASTE MODEL ───────────────────────────────────────────────
if not os.path.exists("models/waste_classifier.pkl"):
    print("\n── Training Waste Model ──────────────────────────────")
    if not os.path.exists("data/raw/smart_waste_data.csv"):
        print("   Generating waste dataset first...")
        # Inline dataset generation
        np.random.seed(42)
        bins_info = [
            {"bin_id":"BIN_001","area":"Saddar",        "bin_type":"General",    "lat":24.8607,"lon":67.0105},
            {"bin_id":"BIN_002","area":"Clifton",        "bin_type":"Recyclable", "lat":24.8138,"lon":67.0300},
            {"bin_id":"BIN_003","area":"Gulshan",        "bin_type":"General",    "lat":24.9215,"lon":67.0977},
            {"bin_id":"BIN_004","area":"North Nazimabad","bin_type":"Organic",    "lat":24.9480,"lon":67.0630},
            {"bin_id":"BIN_005","area":"Korangi",        "bin_type":"General",    "lat":24.8300,"lon":67.1300},
            {"bin_id":"BIN_006","area":"Malir",          "bin_type":"Recyclable", "lat":24.8930,"lon":67.2060},
            {"bin_id":"BIN_007","area":"Lyari",          "bin_type":"Organic",    "lat":24.8558,"lon":66.9922},
            {"bin_id":"BIN_008","area":"DHA",            "bin_type":"General",    "lat":24.7925,"lon":67.0601},
            {"bin_id":"BIN_009","area":"Landhi",         "bin_type":"Recyclable", "lat":24.8560,"lon":67.1900},
            {"bin_id":"BIN_010","area":"PECHS",          "bin_type":"Organic",    "lat":24.8720,"lon":67.0610},
        ]
        from datetime import datetime, timedelta
        fill_rates = {"General":np.random.uniform(8,15),"Recyclable":np.random.uniform(4,9),"Organic":np.random.uniform(6,12)}
        records=[]; start=datetime(2024,1,1)
        for b in bins_info:
            fill=np.random.uniform(0,20)
            base=fill_rates[b['bin_type']]
            for day in range(90):
                cur=start+timedelta(days=day); wknd=cur.weekday()>=5
                for rd in range(6):
                    ts=cur+timedelta(hours=rd*4)
                    fill+=((base*(1.3 if wknd else 1.0))/6)+np.random.normal(0,1.5)
                    fill=np.clip(fill,0,100); collected=fill>=85
                    records.append({"timestamp":ts.strftime("%Y-%m-%d %H:%M:%S"),
                        "bin_id":b['bin_id'],"area":b['area'],"bin_type":b['bin_type'],
                        "latitude":b['lat'],"longitude":b['lon'],
                        "fill_level_%":round(fill,2),"temperature_C":round(np.random.uniform(28,42),1),
                        "humidity_%":round(np.random.uniform(55,90),1),"is_weekend":int(wknd),
                        "collection_needed":int(fill>=75),"collected":int(collected)})
                    if collected: fill=np.random.uniform(0,10)
        os.makedirs("data/raw",exist_ok=True)
        pd.DataFrame(records).to_csv("data/raw/smart_waste_data.csv",index=False)
        print(f"   ✅ Generated {len(records):,} waste records")

    df = pd.read_csv("data/raw/smart_waste_data.csv")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values(['bin_id','timestamp'])
    df['prev_fill_level'] = df.groupby('bin_id')['fill_level_%'].shift(1)
    df['fill_change']     = df['fill_level_%'] - df['prev_fill_level']
    df['hour']            = df['timestamp'].dt.hour
    df['day_of_week']     = df['timestamp'].dt.dayofweek
    df['month']           = df['timestamp'].dt.month
    df['bin_type_code']   = df['bin_type'].map({"General":0,"Recyclable":1,"Organic":2})
    df = df.dropna(subset=['prev_fill_level'])

    WFEATURES = ['prev_fill_level','fill_change','hour','day_of_week','month',
                 'is_weekend','temperature_C','humidity_%','bin_type_code']
    X = df[WFEATURES]
    yc = df['collection_needed']
    yr = df['fill_level_%']
    Xtr,Xte,yct,yce,yrt,yre = train_test_split(X,yc,yr,test_size=.2,random_state=42)

    clf = RandomForestClassifier(n_estimators=100,random_state=42,n_jobs=-1)
    clf.fit(Xtr,yct)
    acc = accuracy_score(yce, clf.predict(Xte))
    print(f"✅ Waste Classifier — Accuracy: {acc:.4f}")

    reg = RandomForestRegressor(n_estimators=100,random_state=42,n_jobs=-1)
    reg.fit(Xtr,yrt)
    r2  = r2_score(yre, reg.predict(Xte))
    mae = mean_absolute_error(yre, reg.predict(Xte))
    print(f"✅ Waste Regressor  — R²: {r2:.4f} | MAE: {mae:.4f}%")

    joblib.dump(clf,      "models/waste_classifier.pkl")
    joblib.dump(reg,      "models/waste_regressor.pkl")
    joblib.dump(WFEATURES,"models/waste_features.pkl")
    df.to_csv("data/processed/waste_clean.csv",index=False)
    print("✅ Saved: models/waste_classifier.pkl + waste_regressor.pkl")
else:
    print("✅ Waste models already exist — skipping")

print("\n" + "=" * 55)
print("  SETUP COMPLETE! All models ready.")
print("=" * 55)
print("""
NEXT STEPS TO DEPLOY:
─────────────────────
1. Make sure these folders exist in your project:
   models/   ← contains all .pkl files
   data/processed/  ← contains cleaned CSVs

2. Create a GitHub account at github.com

3. Create a new repository called: FYP-Urban-AI

4. Upload ALL your project files including models/ folder

5. Go to share.streamlit.io
   → Sign in with GitHub
   → New app → Select your repo
   → Main file: app.py
   → Click Deploy!

6. Your live URL will be:
   https://your-username-fyp-urban-ai.streamlit.app
""")
