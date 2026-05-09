# 🏙️ AI-Driven Sustainable Urban Management System
**GCUF · BSDS Final Year Project 2026**
**Developer:** Ahmad Raza Freed (2022-GCUF-02816)
**Supervisor:** Ms. Rabia Shahid

---

## 🎯 Project Overview
An AI-powered urban management system for Pakistan that provides:
- **Real-time flood prediction** for 24 Pakistani cities using live weather data
- **Heatwave risk monitoring** with temperature analysis
- **Smart waste management** with AI-powered bin fill prediction
- **Route optimization** for waste collection trucks
- **7-day forecasting** for flood and heatwave risks
- **Interactive risk maps** with city-level detail
- **Email alert system** for critical risk notifications
- **PDF report generation** for city officials

---

## 🤖 AI Models
| Model | Algorithm | R² Score | MAE |
|-------|-----------|----------|-----|
| Flood Prediction | GradientBoostingRegressor | 0.9920 | 0.0033 |
| Waste Fill Level | RandomForestRegressor | 0.9998 | 0.19% |
| Waste Collection | RandomForestClassifier | ~99% accuracy | — |

---

## 🌆 Cities Covered (24)
Karachi, Lahore, Islamabad, Faisalabad, Rawalpindi, Peshawar, Multan, Quetta,
Nowshera, Charsadda, Sukkur, Jacobabad, Dadu, Larkana, Shikarpur,
Dera Ghazi Khan, Rajanpur, Muzaffarabad, Swat, Hyderabad, Thatta,
Khairpur, Ghotki, Sialkot

---

## 🚀 Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

**Demo Login Credentials:**
- `admin / admin123` — Full access
- `shahbaz / fyp2026` — Developer
- `supervisor / gcuf2026` — Supervisor view
- `ndma / ndma123` — NDMA Official

---

## 📁 Project Structure
```
FYP_UrbanManagement/
├── app.py                          # Main dashboard
├── requirements.txt                # Dependencies
├── models/
│   ├── flood_model.pkl             # Trained flood model
│   ├── flood_features.pkl          # Feature names
│   ├── waste_classifier.pkl        # Waste collection classifier
│   ├── waste_regressor.pkl         # Waste fill regressor
│   └── waste_features.pkl          # Feature names
├── data/
│   ├── raw/
│   │   ├── flood.csv               # Flood dataset
│   │   └── smart_waste_data.csv    # Waste dataset
│   └── processed/
│       ├── flood_clean.csv         # Cleaned flood data
│       └── waste_clean.csv         # Cleaned waste data
├── database/
│   └── urban.db                    # SQLite alerts database
└── scripts/
    ├── flood_model_v2.py           # Model training script
    ├── waste_model.py              # Waste model training
    └── generate_waste_dataset.py   # Dataset generator
```

---

## 🛠️ Tech Stack
- **Frontend:** Streamlit (Python)
- **ML Models:** Scikit-learn (GradientBoosting, RandomForest)
- **Weather API:** Open-Meteo (free, no key needed)
- **Database:** SQLite
- **Maps:** Folium + Streamlit-Folium
- **PDF:** ReportLab
- **Deployment:** Streamlit Cloud

---

## 📊 Features
- ✅ Login system with 4 user roles
- ✅ Live weather data for all 24 cities
- ✅ Seasonal risk adjustment (monsoon/pre-monsoon/winter)
- ✅ City-specific infrastructure risk profiles
- ✅ Interactive folium maps
- ✅ 7-day flood + heatwave forecast
- ✅ Waste bin monitoring with progress bars
- ✅ Route optimizer (nearest-neighbor TSP)
- ✅ Email alerts via Gmail SMTP
- ✅ PDF report generator
- ✅ SQLite alert history database
- ✅ CSV export for all reports
