# 🚀 Deployment Guide — Streamlit Cloud
## FYP Urban AI System

---

## STEP 1 — Run Setup (one time only)
```
cd FYP_UrbanManagement
python setup_models.py
```
This makes sure all model files are saved and ready.

---

## STEP 2 — Your folder must look like this
```
FYP_UrbanManagement/
├── app.py
├── requirements.txt
├── setup_models.py
├── README.md
├── .streamlit/
│   └── config.toml
├── models/
│   ├── flood_model.pkl        ← MUST exist
│   ├── flood_features.pkl     ← MUST exist
│   ├── waste_classifier.pkl   ← MUST exist
│   ├── waste_regressor.pkl    ← MUST exist
│   └── waste_features.pkl     ← MUST exist
└── data/
    └── processed/
        ├── flood_clean.csv    ← MUST exist
        └── waste_clean.csv    ← MUST exist
```

---

## STEP 3 — Create GitHub Repository
1. Go to **github.com** → Sign up (free)
2. Click **New Repository**
3. Name it: `FYP-Urban-AI`
4. Set to **Public**
5. Click Create

---

## STEP 4 — Upload Files to GitHub
### Easy way (no terminal needed):
1. Open your repo on GitHub
2. Click **uploading an existing file**
3. Drag and drop your ENTIRE FYP_UrbanManagement folder
4. Important: Upload models/ folder too (pkl files)
5. Click **Commit changes**

### If files are too large (pkl files can be big):
- Go to **Git LFS** (Large File Storage) — google "github upload large files"
- Or use GitHub Desktop app (easiest)

---

## STEP 5 — Deploy on Streamlit Cloud
1. Go to **share.streamlit.io**
2. Click **Sign in with GitHub**
3. Click **New app**
4. Select your repository: `FYP-Urban-AI`
5. Branch: `main`
6. Main file path: `app.py`
7. Click **Deploy!**

Wait 2-3 minutes...

---

## STEP 6 — Your Live URL
```
https://[your-github-username]-fyp-urban-ai-app-[random].streamlit.app
```

**Share this with:**
- Your supervisor Ms. Rabia Shahid
- Your FYP committee
- Put it in your FYP report cover page!

---

## ⚠️ Common Issues & Fixes

**Error: ModuleNotFoundError**
→ Make sure requirements.txt has all packages listed

**Error: FileNotFoundError (models)**
→ Make sure models/ folder is uploaded to GitHub

**App crashes on load**
→ Check Streamlit Cloud logs (click "Manage app" → "Logs")

**Models too large to upload**
→ Use GitHub Desktop or Git LFS

---

## 💡 Pro Tips for Your Viva

1. **Open the live URL on your phone** during viva — very impressive
2. **Show login page first** — demonstrates security awareness
3. **Use supervisor/gcuf2026** login in front of supervisor
4. **Click Send Test Email** live during demo — wow factor
5. **Generate PDF report** during viva and show it on screen
6. **Show the map page** — interactive maps always impress committee
