"""
╔══════════════════════════════════════════════════════════════╗
║  AI-DRIVEN SUSTAINABLE URBAN MANAGEMENT SYSTEM               ║
║  GCUF Final Year Project — BSDS 2026                         ║
║  Run: streamlit run app.py                                   ║
╚══════════════════════════════════════════════════════════════╝
pip install streamlit pandas numpy scikit-learn joblib
          matplotlib seaborn folium streamlit-folium requests
"""

import streamlit as st
import hashlib
import urllib.parse
import httpx
import pandas as pd
import numpy as np
import joblib, sqlite3, requests, os, math, warnings
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
warnings.filterwarnings("ignore")

# ═══════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════
st.set_page_config(page_title="Urban AI Pakistan", page_icon="🏙️",
                   layout="wide", initial_sidebar_state="expanded")

# ═══════════════════════════════════════════════════════════════
# CSS — Production dark command-center theme
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');
:root {
  --bg:    #080c14; --card: #0d1421; --hover: #111b2e;
  --bdr:   #1e2d45; --bdrh: #2a4066;
  --txt:   #e8edf5; --txt2: #7a8ea8; --txt3: #3d5170;
  --blue:  #3b82f6; --cyan: #06b6d4; --green: #10b981;
  --amber: #f59e0b; --red:  #ef4444; --purple:#8b5cf6;
  --mono:  'Space Mono', monospace;
  --sans:  'DM Sans', sans-serif;
}
/* ── Base ── */
html,body,.stApp{background:var(--bg);font-family:var(--sans);color:var(--txt)}
[data-testid="stSidebar"]{background:var(--card);border-right:1px solid var(--bdr)}
.block-container{padding:1rem 1.2rem;max-width:1400px}
h1{font-family:var(--mono);letter-spacing:-.02em;font-size:clamp(1.3rem,4vw,2rem)}
h2,h3{font-family:var(--mono);letter-spacing:-.02em;font-size:clamp(1rem,3vw,1.5rem)}
::-webkit-scrollbar{width:4px}::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:var(--bdrh);border-radius:2px}

/* ── Cards ── */
.card{background:var(--card);border:1px solid var(--bdr);border-radius:12px;padding:16px;margin:5px 0}
.kpi{background:var(--card);border:1px solid var(--bdr);border-radius:12px;padding:14px;text-align:center}
.kpi-v{font-family:var(--mono);font-size:clamp(1.4rem,4vw,2rem);font-weight:700;line-height:1}
.kpi-l{font-size:clamp(.6rem,2vw,.75rem);color:var(--txt2);margin-top:5px;text-transform:uppercase;letter-spacing:.06em}

/* ── Alerts ── */
.alert{border-radius:10px;padding:12px 16px;margin:5px 0;border-left:3px solid;font-size:clamp(.78rem,2.5vw,.9rem)}
.a-crit{background:#1a0a0a;border-color:var(--red);color:#fca5a5}
.a-warn{background:#1a1400;border-color:var(--amber);color:#fcd34d}
.a-info{background:#0a1628;border-color:var(--blue);color:#93c5fd}
.a-ok{background:#071a12;border-color:var(--green);color:#6ee7b7}

/* ── Section header ── */
.sec{font-family:var(--mono);font-size:.62rem;letter-spacing:.12em;text-transform:uppercase;
     color:var(--txt3);border-bottom:1px solid var(--bdr);padding-bottom:7px;margin:16px 0 12px}

/* ── Badges ── */
.badge{display:inline-block;font-size:clamp(.6rem,2vw,.68rem);font-family:var(--mono);
       padding:3px 8px;border-radius:20px;margin:2px;white-space:nowrap}
.b-r{background:#2d0f0f;color:#f87171;border:1px solid #7f1d1d}
.b-a{background:#2d1f00;color:#fbbf24;border:1px solid #78350f}
.b-g{background:#062318;color:#34d399;border:1px solid #064e3b}
.b-b{background:#0a1f3d;color:#60a5fa;border:1px solid #1e3a5f}
.b-p{background:#1a0d2e;color:#a78bfa;border:1px solid #4c1d95}

/* ── Prediction box ── */
.pred{border-radius:16px;padding:22px;text-align:center;border:2px solid;margin:8px 0}
.pred-n{font-family:var(--mono);font-size:clamp(2.2rem,8vw,3.5rem);font-weight:700;line-height:1.1}

/* ── Progress bar ── */
.prog-w{background:var(--bdr);border-radius:4px;height:6px;margin:4px 0;overflow:hidden}
.prog-f{height:100%;border-radius:4px}

/* ── Streamlit overrides ── */
div[data-testid="stMetric"]{background:var(--card);border:1px solid var(--bdr);border-radius:10px;padding:10px 14px}
div[data-testid="stMetric"] label{color:var(--txt2)!important;font-size:.78rem!important}
.stButton>button{background:var(--hover);border:1px solid var(--bdrh);color:var(--txt);
                 border-radius:8px;width:100%;font-size:clamp(.8rem,2.5vw,.9rem)}
.stButton>button:hover{background:var(--blue);border-color:var(--blue);color:white}
.stButton>button[kind="primary"]{background:var(--blue);border-color:var(--blue);color:white}
.stTabs [data-baseweb="tab-list"]{background:var(--card);border-radius:8px}
.stTabs [data-baseweb="tab"]{color:var(--txt2);font-size:clamp(.78rem,2.5vw,.9rem)}
.stTabs [aria-selected="true"]{color:var(--txt)}
div[data-testid="stExpander"]{background:var(--card);border:1px solid var(--bdr);border-radius:8px}
div[data-testid="stExpander"] summary{font-size:clamp(.82rem,2.5vw,.92rem)}
.stSelectbox label,.stSlider label,.stTextInput label{font-size:clamp(.78rem,2.5vw,.88rem)!important;color:var(--txt2)!important}
#MainMenu,footer,header{visibility:hidden}

/* ── Mobile responsive ── */
@media (max-width:768px){
  .block-container{padding:.8rem .8rem}
  .card{padding:12px}
  .kpi{padding:12px 8px}
  .pred{padding:18px 12px}
  [data-testid="stSidebar"]{width:80vw!important}
  .stButton>button{font-size:.82rem;padding:8px 12px}
  h1{font-size:1.3rem!important}
  .badge{font-size:.6rem;padding:2px 6px}
}
@media (max-width:480px){
  .block-container{padding:.6rem .6rem}
  .kpi-v{font-size:1.4rem}
  .pred-n{font-size:2rem}
}
</style>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# CITIES DATA
# ═══════════════════════════════════════════════════════════════
CITIES = {
    "Karachi":         {"lat":24.8607,"lon":67.0105,"province":"Sindh",       "pop":"16M",  "coastal":True,  "reason":"Coastal city, monsoon flooding, poor drainage"},
    "Lahore":          {"lat":31.5497,"lon":74.3436,"province":"Punjab",      "pop":"14M",  "coastal":False, "reason":"River Ravi flooding, urban drainage issues"},
    "Islamabad":       {"lat":33.6844,"lon":73.0479,"province":"Federal",     "pop":"2M",   "coastal":False, "reason":"Hill torrents, flash floods from Margalla Hills"},
    "Faisalabad":      {"lat":31.4504,"lon":73.1350,"province":"Punjab",      "pop":"4M",   "coastal":False, "reason":"River flooding, agricultural drainage"},
    "Rawalpindi":      {"lat":33.5651,"lon":73.0169,"province":"Punjab",      "pop":"2.5M", "coastal":False, "reason":"Nullah Lai flash floods, urban flooding"},
    "Peshawar":        {"lat":34.0151,"lon":71.5249,"province":"KPK",         "pop":"2M",   "coastal":False, "reason":"River Kabul flooding, monsoon torrents"},
    "Multan":          {"lat":30.1978,"lon":71.4711,"province":"Punjab",      "pop":"2M",   "coastal":False, "reason":"River Chenab and Sutlej flooding"},
    "Quetta":          {"lat":30.1798,"lon":66.9750,"province":"Balochistan", "pop":"1M",   "coastal":False, "reason":"Flash floods, poor drainage infrastructure"},
    "Nowshera":        {"lat":34.0153,"lon":71.9747,"province":"KPK",         "pop":"300K", "coastal":False, "reason":"River Kabul and Swat confluence, most flood-hit"},
    "Charsadda":       {"lat":34.1453,"lon":71.7308,"province":"KPK",         "pop":"200K", "coastal":False, "reason":"2010 and 2022 mega floods, River Swat overflow"},
    "Sukkur":          {"lat":27.7052,"lon":68.8574,"province":"Sindh",       "pop":"500K", "coastal":False, "reason":"River Indus flood gateway to lower Sindh"},
    "Jacobabad":       {"lat":28.2769,"lon":68.4516,"province":"Sindh",       "pop":"200K", "coastal":False, "reason":"2022 floods, 90% submerged, hottest city on earth"},
    "Dadu":            {"lat":26.7319,"lon":67.7751,"province":"Sindh",       "pop":"150K", "coastal":False, "reason":"2022 completely inundated, very low elevation"},
    "Larkana":         {"lat":27.5570,"lon":68.2247,"province":"Sindh",       "pop":"490K", "coastal":False, "reason":"River Indus, 2022 catastrophic floods"},
    "Shikarpur":       {"lat":27.9554,"lon":68.6382,"province":"Sindh",       "pop":"180K", "coastal":False, "reason":"Repeated Indus flooding, poor flood defenses"},
    "Dera Ghazi Khan": {"lat":30.0564,"lon":70.6340,"province":"Punjab",      "pop":"470K", "coastal":False, "reason":"River Indus and hill torrents, 2010 worst hit"},
    "Rajanpur":        {"lat":29.1042,"lon":70.3298,"province":"Punjab",      "pop":"200K", "coastal":False, "reason":"Downstream Indus floods every monsoon season"},
    "Muzaffarabad":    {"lat":34.3700,"lon":73.4710,"province":"AJK",         "pop":"120K", "coastal":False, "reason":"River Jhelum, glacial lake outburst floods"},
    "Swat":            {"lat":35.2227,"lon":72.4258,"province":"KPK",         "pop":"250K", "coastal":False, "reason":"2010 floods destroyed 70 percent of valley"},
    "Hyderabad":       {"lat":25.3960,"lon":68.3578,"province":"Sindh",       "pop":"1.7M", "coastal":False, "reason":"Lower Indus flooding, 2022 major impact"},
    "Thatta":          {"lat":24.7461,"lon":67.9239,"province":"Sindh",       "pop":"100K", "coastal":True,  "reason":"Coastal and Indus delta flooding, sea intrusion"},
    "Khairpur":        {"lat":27.5295,"lon":68.7585,"province":"Sindh",       "pop":"350K", "coastal":False, "reason":"River Indus right bank, annually flooded"},
    "Ghotki":          {"lat":28.0057,"lon":69.3160,"province":"Sindh",       "pop":"200K", "coastal":False, "reason":"Upper Sindh Indus flooding, poor embankments"},
    "Sialkot":         {"lat":32.4945,"lon":74.5229,"province":"Punjab",      "pop":"655K", "coastal":False, "reason":"River Chenab flooding, urban drainage issues"},
}

PROFILES = {
    "Karachi":         dict(i=7,u=8,d=7,p=7,df=3,e=7,ag=2,t=6,r=4,c=9,l=1,w=4,s=5,po=9,wl=6,cl=6,pt=6,pr=6),
    "Lahore":          dict(i=5,u=8,d=6,p=6,df=4,e=7,ag=5,t=4,r=7,c=0,l=1,w=5,s=6,po=9,wl=5,cl=5,pt=5,pr=5),
    "Islamabad":       dict(i=3,u=5,d=3,p=3,df=4,e=4,ag=2,t=7,r=4,c=0,l=5,w=6,s=4,po=4,wl=4,cl=5,pt=3,pr=3),
    "Faisalabad":      dict(i=5,u=7,d=6,p=6,df=4,e=6,ag=7,t=4,r=6,c=0,l=1,w=5,s=6,po=8,wl=5,cl=5,pt=5,pr=5),
    "Rawalpindi":      dict(i=5,u=7,d=7,p=6,df=3,e=6,ag=3,t=6,r=6,c=0,l=3,w=5,s=5,po=7,wl=4,cl=5,pt=4,pr=4),
    "Peshawar":        dict(i=6,u=6,d=7,p=7,df=6,e=7,ag=5,t=6,r=8,c=0,l=4,w=6,s=7,po=7,wl=5,cl=6,pt=7,pr=7),
    "Multan":          dict(i=6,u=6,d=7,p=7,df=5,e=6,ag=7,t=5,r=8,c=0,l=1,w=6,s=7,po=7,wl=6,cl=6,pt=6,pr=6),
    "Quetta":          dict(i=6,u=5,d=7,p=6,df=5,e=5,ag=4,t=7,r=5,c=0,l=5,w=6,s=5,po=5,wl=4,cl=6,pt=6,pr=6),
    "Nowshera":        dict(i=8,u=5,d=8,p=8,df=7,e=7,ag=6,t=7,r=9,c=0,l=4,w=8,s=8,po=5,wl=7,cl=7,pt=8,pr=8),
    "Charsadda":       dict(i=8,u=5,d=8,p=8,df=7,e=7,ag=7,t=6,r=9,c=0,l=3,w=8,s=8,po=5,wl=7,cl=7,pt=8,pr=8),
    "Sukkur":          dict(i=7,u=5,d=8,p=8,df=5,e=7,ag=7,t=3,r=9,c=0,l=1,w=8,s=8,po=6,wl=7,cl=7,pt=8,pr=7),
    "Jacobabad":       dict(i=9,u=4,d=9,p=9,df=6,e=7,ag=8,t=2,r=8,c=0,l=1,w=9,s=8,po=4,wl=8,cl=9,pt=9,pr=9),
    "Dadu":            dict(i=9,u=3,d=9,p=9,df=5,e=6,ag=8,t=2,r=9,c=0,l=1,w=9,s=9,po=3,wl=8,cl=8,pt=9,pr=9),
    "Larkana":         dict(i=8,u=5,d=8,p=8,df=5,e=7,ag=7,t=3,r=9,c=0,l=1,w=8,s=8,po=6,wl=7,cl=7,pt=8,pr=8),
    "Shikarpur":       dict(i=8,u=4,d=8,p=8,df=5,e=7,ag=7,t=3,r=8,c=0,l=1,w=8,s=8,po=4,wl=7,cl=7,pt=8,pr=8),
    "Dera Ghazi Khan": dict(i=7,u=5,d=8,p=8,df=6,e=7,ag=7,t=6,r=8,c=0,l=3,w=7,s=7,po=6,wl=6,cl=7,pt=7,pr=7),
    "Rajanpur":        dict(i=8,u=4,d=8,p=8,df=6,e=7,ag=7,t=3,r=9,c=0,l=1,w=8,s=8,po=4,wl=7,cl=7,pt=8,pr=8),
    "Muzaffarabad":    dict(i=7,u=4,d=7,p=7,df=7,e=5,ag=4,t=9,r=9,c=0,l=8,w=8,s=7,po=3,wl=6,cl=7,pt=6,pr=6),
    "Swat":            dict(i=7,u=4,d=7,p=7,df=8,e=6,ag=6,t=8,r=9,c=0,l=7,w=8,s=7,po=4,wl=7,cl=7,pt=7,pr=7),
    "Hyderabad":       dict(i=7,u=7,d=7,p=7,df=4,e=7,ag=6,t=3,r=8,c=0,l=1,w=7,s=7,po=8,wl=7,cl=7,pt=7,pr=7),
    "Thatta":          dict(i=8,u=3,d=8,p=8,df=5,e=5,ag=7,t=2,r=8,c=9,l=1,w=8,s=8,po=3,wl=8,cl=8,pt=8,pr=8),
    "Khairpur":        dict(i=8,u=4,d=8,p=8,df=5,e=7,ag=7,t=3,r=9,c=0,l=1,w=8,s=8,po=5,wl=7,cl=7,pt=8,pr=8),
    "Ghotki":          dict(i=7,u=4,d=8,p=7,df=5,e=6,ag=7,t=3,r=8,c=0,l=1,w=7,s=7,po=4,wl=7,cl=7,pt=7,pr=7),
    "Sialkot":         dict(i=5,u=6,d=6,p=6,df=4,e=6,ag=6,t=4,r=7,c=0,l=1,w=5,s=6,po=7,wl=5,cl=5,pt=5,pr=5),
}

def get_sliders(city):
    p = PROFILES.get(city, {k:5 for k in 'i u d p df e ag t r c l w s po wl cl pt pr'.split()})
    return dict(infrastructure=p['i'],urbanization=p['u'],drainage=p['d'],dams=p['i'],
                deforestation=p['df'],encroachments=p['e'],agriculture=p['ag'],
                planning=p['p'],political=p['pt'],preparedness=p['pr'],
                topography=p['t'],river=p['r'],coastal=p['c'],landslide=p['l'],
                watersheds=p['w'],siltation=p['s'],population=p['po'],
                wetland_loss=p['wl'],climate_change=p['cl'])

# ═══════════════════════════════════════════════════════════════
# SEASON ENGINE
# ═══════════════════════════════════════════════════════════════
def get_season():
    m = datetime.now().month
    if   m in [6,7,8,9]:  return {"name":"Monsoon",    "fm":1.0, "hm":1.0, "e":"🌧️","c":"#ef4444","w":None}
    elif m in [4,5]:       return {"name":"Pre-Monsoon","fm":0.35,"hm":1.2, "e":"☀️","c":"#f59e0b","w":"Pre-monsoon: Flood risk is low. Heatwave risk is elevated."}
    elif m in [10,11]:     return {"name":"Post-Monsoon","fm":0.5,"hm":0.6,"e":"🌦️","c":"#f59e0b","w":"Post-monsoon: Residual river flood risk."}
    else:                  return {"name":"Winter",     "fm":0.2, "hm":0.3, "e":"❄️","c":"#10b981","w":"Winter: Very low flood risk."}

# ═══════════════════════════════════════════════════════════════
# WEATHER API
# ═══════════════════════════════════════════════════════════════
@st.cache_data(ttl=600)
def get_weather(city):
    c   = CITIES[city]
    url = (f"https://api.open-meteo.com/v1/forecast?latitude={c['lat']}&longitude={c['lon']}"
           f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,"
           f"precipitation,rain,wind_speed_10m,weather_code"
           f"&hourly=precipitation_probability,temperature_2m"
           f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,"
           f"precipitation_probability_max,weathercode"
           f"&forecast_days=7&timezone=Asia%2FKarachi")
    try:
        r = requests.get(url, timeout=8)
        if r.status_code == 200:
            d = r.json(); cu = d['current']
            return {"temp":round(cu['temperature_2m'],1),"feels":round(cu['apparent_temperature'],1),
                    "hum":cu['relative_humidity_2m'],"precip":cu['precipitation'],"rain":cu['rain'],
                    "wind":cu['wind_speed_10m'],"rp":max(d['hourly']['precipitation_probability'][:6]),
                    "code":cu['weather_code'],"fc":d['daily'],"live":True}
    except: pass
    return {"temp":35,"feels":38,"hum":60,"precip":0,"rain":0,"wind":12,"rp":10,"code":0,"fc":None,"live":False}

def wemoji(c):
    if c==0: return "☀️"
    elif c in [1,2,3]: return "🌤️"
    elif c in [45,48]: return "🌫️"
    elif c in [51,53,55,61,63,65]: return "🌧️"
    elif c in [80,81,82]: return "⛈️"
    elif c in [95,96,99]: return "🌩️"
    return "🌡️"

def rcol(v):
    return "#ef4444" if v>=65 else "#f59e0b" if v>=40 else "#10b981"

# ═══════════════════════════════════════════════════════════════
# MODELS
# ═══════════════════════════════════════════════════════════════
@st.cache_resource
def load_models():
    try:
        return (joblib.load("models/flood_model.pkl"),
                joblib.load("models/flood_features.pkl"),
                joblib.load("models/waste_classifier.pkl"),
                joblib.load("models/waste_regressor.pkl"),
                joblib.load("models/waste_features.pkl"))
    except FileNotFoundError as e:
        st.error(f"Model file not found: {e}. Please run setup_models.py first.")
        st.stop()

FM, FF, WC, WR, WF = load_models()

def flood_risk(city, w, s=None):
    if s is None: s = get_sliders(city)
    season = get_season()
    c = CITIES[city]
    mn = min(10, (w['precip']/5) + (w['rp']/15))
    raw = {
        'MonsoonIntensity':mn,'TopographyDrainage':s['topography'],
        'RiverManagement':s['river'],'Deforestation':s['deforestation'],
        'Urbanization':s['urbanization'],'ClimateChange':s['climate_change'],
        'DamsQuality':s['dams'],'Siltation':s['siltation'],
        'AgriculturalPractices':s['agriculture'],'Encroachments':s['encroachments'],
        'IneffectiveDisasterPreparedness':s['preparedness'],
        'DrainageSystems':s['drainage'],
        'CoastalVulnerability':9 if c['coastal'] else s['coastal'],
        'Landslides':s['landslide'],'Watersheds':s['watersheds'],
        'DeterioratingInfrastructure':s['infrastructure'],
        'PopulationScore':s['population'],'WetlandLoss':s['wetland_loss'],
        'InadequatePlanning':s['planning'],'PoliticalFactors':s['political'],
    }
    raw['Infrastructure_Risk']=(raw['DeterioratingInfrastructure']+raw['DrainageSystems']+raw['DamsQuality'])/3
    raw['Human_Activity_Risk']=(raw['Deforestation']+raw['Urbanization']+raw['AgriculturalPractices']+raw['Encroachments'])/4
    raw['Climate_Risk']=(raw['MonsoonIntensity']+raw['ClimateChange']+raw['WetlandLoss'])/3
    raw['Governance_Risk']=(raw['IneffectiveDisasterPreparedness']+raw['InadequatePlanning']+raw['PoliticalFactors'])/3
    raw['Total_Risk_Score']=raw['Infrastructure_Risk']+raw['Human_Activity_Risk']+raw['Climate_Risk']+raw['Governance_Risk']
    return float(np.clip(FM.predict(pd.DataFrame([raw])[FF])[0]*season['fm'],0,1))

def heat_risk(w, city):
    season = get_season()
    t,fl,h = w['temp'],w['feels'],w['hum']
    p = PROFILES.get(city,{})
    sc = 0
    if t>=48: sc+=40
    elif t>=45: sc+=30
    elif t>=42: sc+=20
    elif t>=38: sc+=10
    elif t>=35: sc+=5
    if fl>t+3: sc+=8
    if h>60 and t>35: sc+=10
    elif h>40 and t>38: sc+=5
    sc += int(p.get('po',5)*1.5)
    if city=="Jacobabad": sc=min(100,sc+20)
    return min(100, round(sc*season['hm'],1))

def hlabel(s):
    if s>=70: return "EXTREME","#ef4444","🔴"
    elif s>=50: return "HIGH","#f59e0b","🟠"
    elif s>=30: return "MODERATE","#eab308","🟡"
    return "LOW","#10b981","🟢"

# ═══════════════════════════════════════════════════════════════
# WASTE DATA
# ═══════════════════════════════════════════════════════════════
@st.cache_data
def load_waste():
    try:
        df = pd.read_csv("data/processed/waste_clean.csv")
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except FileNotFoundError:
        st.error("waste_clean.csv not found. Please run setup_models.py first.")
        st.stop()

WDF = load_waste()

# ═══════════════════════════════════════════════════════════════
# ROUTE OPTIMIZER
# ═══════════════════════════════════════════════════════════════
def haversine(la1,lo1,la2,lo2):
    R=6371; dlat=math.radians(la2-la1); dlon=math.radians(lo2-lo1)
    a=math.sin(dlat/2)**2+math.cos(math.radians(la1))*math.cos(math.radians(la2))*math.sin(dlon/2)**2
    return R*2*math.asin(math.sqrt(a))

def optimize_route(df):
    bins = df[df["collection_needed"]==1].copy()
    if len(bins)==0: return [],0.0
    bin_list = bins.to_dict("records")
    visited,route,total=set(),[],0.0
    cur=bin_list[0]; route.append(cur); visited.add(cur["bin_id"])
    while len(visited)<len(bin_list):
        best,bbin=float("inf"),None
        for b in bin_list:
            if b["bin_id"] in visited: continue
            d=haversine(cur["latitude"],cur["longitude"],b["latitude"],b["longitude"])
            if d<best: best,bbin=d,b
        if bbin is None: break
        total+=best; route.append(bbin); visited.add(bbin["bin_id"]); cur=bbin
    return route,total

# ═══════════════════════════════════════════════════════════════
# DATABASE
# ═══════════════════════════════════════════════════════════════
def init_db():
    os.makedirs("database",exist_ok=True)
    conn=sqlite3.connect("database/urban.db")
    conn.execute("""CREATE TABLE IF NOT EXISTS flood_alerts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,ts TEXT,city TEXT,
        prob REAL,risk TEXT,temp REAL,humidity REAL,precip REAL,heat REAL,live INTEGER)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS waste_alerts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,ts TEXT,
        bin_id TEXT,area TEXT,fill REAL,needed INTEGER)""")
    conn.commit(); conn.close()

def db_flood(city,prob,risk,w,heat):
    conn=sqlite3.connect("database/urban.db")
    conn.execute("INSERT INTO flood_alerts VALUES(NULL,?,?,?,?,?,?,?,?,?)",
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),city,round(prob,4),
         risk,w['temp'],w['hum'],w['precip'],round(heat,1),int(w['live'])))
    conn.commit(); conn.close()

def db_waste(bin_id,area,fill,needed):
    conn=sqlite3.connect("database/urban.db")
    conn.execute("INSERT INTO waste_alerts VALUES(NULL,?,?,?,?,?)",
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),bin_id,area,fill,needed))
    conn.commit(); conn.close()

def db_get(tbl,n=25):
    conn=sqlite3.connect("database/urban.db")
    try: df=pd.read_sql(f"SELECT * FROM {tbl} ORDER BY id DESC LIMIT {n}",conn)
    except: df=pd.DataFrame()
    conn.close(); return df

init_db()

# ═══════════════════════════════════════════════════════════════
# CHART HELPER
# ═══════════════════════════════════════════════════════════════
def dfig(w=10,h=4):
    fig,ax=plt.subplots(figsize=(w,h))
    fig.patch.set_facecolor('#080c14'); ax.set_facecolor('#0d1421')
    ax.tick_params(colors='#7a8ea8'); ax.spines[:].set_color('#1e2d45')
    ax.xaxis.label.set_color('#7a8ea8'); ax.yaxis.label.set_color('#7a8ea8')
    return fig,ax

# ═══════════════════════════════════════════════════════════════
# LOGIN SYSTEM
# ═══════════════════════════════════════════════════════════════
# ── Auth0 Config ─────────────────────────────────────────────
try:
    AUTH0_DOMAIN        = st.secrets["AUTH0_DOMAIN"]
    AUTH0_CLIENT_ID     = st.secrets["AUTH0_CLIENT_ID"]
    AUTH0_CLIENT_SECRET = st.secrets["AUTH0_CLIENT_SECRET"]
    AUTH0_ENABLED = True
except Exception:
    AUTH0_ENABLED = False

REDIRECT_URI    = "https://fyp-urban-ai-awuuxpxukxr6kcd8qhfr8f.streamlit.app/"

def get_google_url():
    if not AUTH0_ENABLED: return "#"
    p = {"response_type":"code","client_id":AUTH0_CLIENT_ID,
         "redirect_uri":REDIRECT_URI,"scope":"openid email profile",
         "connection":"google-oauth2"}
    return f"https://{AUTH0_DOMAIN}/authorize?{urllib.parse.urlencode(p)}"

def get_email_url():
    if not AUTH0_ENABLED: return "#"
    p = {"response_type":"code","client_id":AUTH0_CLIENT_ID,
         "redirect_uri":REDIRECT_URI,"scope":"openid email profile"}
    return f"https://{AUTH0_DOMAIN}/authorize?{urllib.parse.urlencode(p)}"

def get_logout_url():
    if not AUTH0_ENABLED: return REDIRECT_URI
    p = {"client_id":AUTH0_CLIENT_ID,"returnTo":REDIRECT_URI}
    return f"https://{AUTH0_DOMAIN}/v2/logout?{urllib.parse.urlencode(p)}"

def exchange_code(code):
    try:
        r = httpx.post(f"https://{AUTH0_DOMAIN}/oauth/token", data={
            "grant_type":"authorization_code","client_id":AUTH0_CLIENT_ID,
            "client_secret":AUTH0_CLIENT_SECRET,"code":code,
            "redirect_uri":REDIRECT_URI}, timeout=10)
        return r.json() if r.status_code==200 else None
    except: return None

def get_userinfo(token):
    try:
        r = httpx.get(f"https://{AUTH0_DOMAIN}/userinfo",
                      headers={"Authorization":f"Bearer {token}"}, timeout=10)
        return r.json() if r.status_code==200 else None
    except: return None

# ── Handle OAuth callback ─────────────────────────────────────
if "auth_user" not in st.session_state:
    st.session_state.auth_user = None

qp = st.query_params
auth_code_param = qp.get("code", None)

if auth_code_param and not st.session_state.auth_user and AUTH0_ENABLED:
    with st.spinner("Signing you in..."):
        tok = exchange_code(auth_code_param)
        if tok and "access_token" in tok:
            info = get_userinfo(tok["access_token"])
            if info:
                st.session_state.auth_user = {
                    "name":    info.get("name","User"),
                    "email":   info.get("email",""),
                    "picture": info.get("picture",""),
                    "role":    "User",
                }
                st.query_params.clear()
                st.rerun()

# ── Show login page ───────────────────────────────────────────
if not st.session_state.auth_user:
    st.markdown("""
    <style>
    .stApp{background:#080c14}
    .lw{display:flex;justify-content:center;align-items:center;min-height:88vh}
    .lb{background:#0d1421;border:1px solid #1e2d45;border-radius:20px;
        padding:44px 38px;width:100%;max-width:400px;text-align:center}
    .lt{font-family:monospace;font-size:1.4rem;font-weight:700;color:#e8edf5;margin:8px 0 4px}
    .ls{color:#7a8ea8;font-size:.85rem;margin-bottom:28px;line-height:1.6}
    .bg{display:flex;align-items:center;justify-content:center;gap:10px;
        background:#fff;color:#1a1a1a;border-radius:10px;padding:13px;
        font-size:.92rem;font-weight:600;text-decoration:none;margin-bottom:14px;
        transition:background .2s}
    .bg:hover{background:#f0f0f0}
    .be{display:flex;align-items:center;justify-content:center;gap:10px;
        background:#3b82f6;color:#fff;border-radius:10px;padding:13px;
        font-size:.92rem;font-weight:600;text-decoration:none;
        transition:background .2s}
    .be:hover{background:#2563eb}
    .div{display:flex;align-items:center;gap:10px;margin:16px 0;color:#3d5170;font-size:.78rem}
    .div::before,.div::after{content:'';flex:1;height:1px;background:#1e2d45}
    .lf{color:#3d5170;font-size:.72rem;margin-top:20px;line-height:1.8}
    </style>
    """, unsafe_allow_html=True)

    google_url = get_google_url()
    email_url  = get_email_url()

    st.markdown(f"""
    <div class="lw"><div class="lb">
      <div style="font-size:2.8rem">🏙️</div>
      <div class="lt">Urban AI System</div>
      <div class="ls">Pakistan · GCUF BSDS 2026<br>AI-Driven Urban Management</div>
      <a href="{google_url}" class="bg" target="_self">
        <svg width="18" height="18" viewBox="0 0 48 48">
          <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>
          <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>
          <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>
          <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/>
        </svg>
        Continue with Google
      </a>
      <div class="div">or</div>
      <a href="{email_url}" class="be" target="_self">
        📧 Login / Sign up with Email
      </a>
      <div class="lf">
        Secure login powered by Auth0 🔒<br>
        Your data is protected and encrypted
      </div>
    </div></div>
    """, unsafe_allow_html=True)
    st.stop()

# ═══════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════
season = get_season()
with st.sidebar:
    st.markdown(f"""
    <div style="padding:12px 0 8px">
      <div style="font-family:'Space Mono',monospace;font-size:.58rem;letter-spacing:.2em;color:#3d5170;text-transform:uppercase">GCUF · BSDS 2026</div>
      <div style="font-family:'Space Mono',monospace;font-size:1rem;font-weight:700;color:#e8edf5;margin-top:4px;line-height:1.3">Urban AI<br>Management</div>
      <div style="font-size:.72rem;color:#3b82f6;margin-top:4px">Pakistan · 24 Cities · Live Weather</div>
    </div>
    <div style="background:#0d1421;border:1px solid #1e2d45;border-radius:8px;padding:9px 12px;margin:8px 0;font-size:.76rem">
      {season['e']} <b style="color:{season['c']}">{season['name']}</b><br>
      <span style="color:#3d5170">{datetime.now().strftime('%d %b %Y · %H:%M')}</span>
    </div>""", unsafe_allow_html=True)

    u = st.session_state.auth_user or {}
    name    = u.get('name','User')
    email   = u.get('email','')
    picture = u.get('picture','')
    pic_html = f'<img src="{picture}" width="28" height="28" style="border-radius:50%;margin-right:8px;vertical-align:middle">' if picture else "👤"
    st.markdown(f"""
    <div style="background:#071a12;border:1px solid #064e3b;border-radius:8px;
                padding:9px 12px;margin:8px 0;font-size:.76rem;display:flex;align-items:center">
      {pic_html}
      <div>
        <b style="color:#34d399">{name}</b><br>
        <span style="color:#3d5170;font-size:.68rem">{email}</span>
      </div>
    </div>""", unsafe_allow_html=True)

    page = st.radio("", [
        "🏠  Overview",
        "🌊  Flood Prediction",
        "🌡️  Heatwave Alert",
        "📅  7-Day Forecast",
        "🗺️  Risk Map",
        "🗑️  Waste Monitor",
        "🚛  Route Optimizer",
        "📊  Model Performance",
        "📧  Email Alerts",
        "📄  PDF Report",
        "🗄️  Alert History",
    ], label_visibility="collapsed")

    st.markdown("---")
    logout_url = get_logout_url()
    st.markdown(f'<a href="{logout_url}" target="_self" style="display:block;background:#1a0a0a;color:#f87171;border:1px solid #7f1d1d;border-radius:8px;padding:8px;text-align:center;text-decoration:none;font-size:.85rem;margin-top:8px">🚪 Logout</a>', unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size:.7rem;color:#3d5170;line-height:2;margin-top:12px">
      <b style="color:#1e2d45">Models</b><br>
      🌊 GradientBoosting · R²=0.99<br>
      🗑️ RandomForest · R²=0.9998<br>
      <b style="color:#1e2d45">Data</b><br>
      🌐 Open-Meteo API (live)<br>
      🗄️ SQLite (alerts DB)
    </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# PAGE: OVERVIEW
# ═══════════════════════════════════════════════════════════════
if "Overview" in page:
    st.markdown("# AI-Driven Urban Management System")
    st.markdown(f"##### Pakistan · 24 cities · {season['e']} {season['name']} · Live weather data")
    if season['w']:
        st.markdown(f'<div class="alert a-warn">⚠️ {season["w"]}</div>',unsafe_allow_html=True)

    latest=WDF.sort_values('timestamp').groupby('bin_id').last().reset_index()
    # KPI — responsive grid via HTML (works on mobile too)
    crit = int((latest["fill_level_%"]>=85).sum())
    high = int(((latest["fill_level_%"]>=70)&(latest["fill_level_%"]<85)).sum())
    st.markdown(f"""
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px;margin:12px 0">
      <div class="kpi"><div class="kpi-v" style="color:#3b82f6">24</div><div class="kpi-l">Cities Monitored</div></div>
      <div class="kpi"><div class="kpi-v" style="color:#ef4444">{crit}</div><div class="kpi-l">Critical Bins</div></div>
      <div class="kpi"><div class="kpi-v" style="color:#f59e0b">{high}</div><div class="kpi-l">High Fill Bins</div></div>
      <div class="kpi"><div class="kpi-v" style="color:#10b981">0.992</div><div class="kpi-l">Flood R²</div></div>
      <div class="kpi"><div class="kpi-v" style="color:#8b5cf6">0.9998</div><div class="kpi-l">Waste R²</div></div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec">Live City Conditions — All 24 Cities</div>',unsafe_allow_html=True)

    # Responsive CSS grid — auto adjusts from 1 col (mobile) to 4 col (desktop)
    city_cards_html = '<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px;margin:8px 0">'
    for cn,ci in CITIES.items():
        w=get_weather(cn)
        fr=flood_risk(cn,w)*100; hr=heat_risk(w,cn)
        _,hc,_=hlabel(hr); frc=rcol(fr)
        live="🟢" if w['live'] else "🟡"
        fb = 'b-r' if fr>=65 else 'b-a' if fr>=40 else 'b-g'
        hb = 'b-r' if hr>=70 else 'b-a' if hr>=50 else 'b-g'
        city_cards_html += f"""
        <div class="card" style="min-width:0">
          <div style="display:flex;justify-content:space-between;align-items:start;flex-wrap:wrap;gap:4px">
            <b style="color:#e8edf5;font-size:.88rem">{cn}</b>
            <span style="font-size:.6rem;color:#3d5170">{live} {ci['province']}</span>
          </div>
          <div style="margin:5px 0">
            {wemoji(w['code'])} <b style="color:#e8edf5;font-family:monospace">{w['temp']}°C</b>
            <span style="color:#3d5170;font-size:.7rem"> /{w['feels']}°C</span>
          </div>
          <div style="margin-bottom:6px;display:flex;flex-wrap:wrap;gap:3px">
            <span class="badge b-b">💧{w['hum']}%</span>
            <span class="badge b-b">🌧️{w['rp']}%</span>
          </div>
          <div style="display:flex;flex-wrap:wrap;gap:3px">
            <span class="badge {fb}">🌊 {fr:.0f}%</span>
            <span class="badge {hb}">🌡️ {hr:.0f}%</span>
          </div>
        </div>"""
    city_cards_html += '</div>'
    st.markdown(city_cards_html, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# PAGE: FLOOD PREDICTION
# ═══════════════════════════════════════════════════════════════
elif "Flood" in page:
    st.markdown("# 🌊 Flood Prediction Module")
    st.markdown("GradientBoosting model · R²=0.9920 · MAE=0.0033 · 25 features · Seasonal-adjusted")
    if season['w']: st.markdown(f'<div class="alert a-warn">{season["e"]} {season["w"]}</div>',unsafe_allow_html=True)
    st.markdown("---")
    # On mobile streamlit stacks columns automatically
    cl,cr=st.columns([1,1])
    with cl:
        city=st.selectbox("Select City",list(CITIES.keys()))
        cp=get_sliders(city); ci=CITIES[city]
        with st.spinner("Fetching live weather..."): w=get_weather(city)
        lt="🟢 Live" if w['live'] else "🟡 Fallback"
        st.markdown(f"""
        <div class="card">
          <div style="display:flex;justify-content:space-between">
            <b style="color:#3b82f6">📡 {city} — Current Weather</b>
            <span style="color:#10b981;font-size:.75rem">{lt}</span>
          </div>
          <div style="margin:10px 0">
            <span style="font-size:1.6rem">{wemoji(w['code'])}</span>
            <b style="font-family:'Space Mono',monospace;font-size:1.5rem;color:#e8edf5"> {w['temp']}°C</b>
            <span style="color:#3d5170"> feels {w['feels']}°C</span>
          </div>
          <div>
            <span class="badge b-b">💧{w['hum']}%</span>
            <span class="badge b-b">🌧️{w['rp']}% rain</span>
            <span class="badge b-b">💨{w['wind']}km/h</span>
            <span class="badge b-b">🌡️{w['precip']}mm</span>
          </div>
          <div style="font-size:.75rem;color:#3d5170;margin-top:8px">
            ℹ️ Sliders pre-filled with {city}'s real infrastructure profile
          </div>
        </div>""",unsafe_allow_html=True)

        with st.expander("🏗️ Infrastructure"):
            drainage=st.slider("Drainage Quality",0,10,cp['drainage'])
            dams=st.slider("Dams Quality",0,10,cp['dams'])
            infra=st.slider("Deteriorating Infrastructure",0,10,cp['infrastructure'])
        with st.expander("🏙️ Urban & Human"):
            urban=st.slider("Urbanization",0,10,cp['urbanization'])
            deforest=st.slider("Deforestation",0,10,cp['deforestation'])
            encroach=st.slider("Encroachments",0,10,cp['encroachments'])
            agri=st.slider("Agricultural Practices",0,10,cp['agriculture'])
        with st.expander("🏛️ Governance"):
            planning=st.slider("Inadequate Planning",0,10,cp['planning'])
            political=st.slider("Political Factors",0,10,cp['political'])
            prep=st.slider("Ineffective Preparedness",0,10,cp['preparedness'])
        with st.expander("🌍 Geographic & Climate"):
            topo=st.slider("Topography",0,10,cp['topography'])
            river=st.slider("River Management",0,10,cp['river'])
            coastal=st.slider("Coastal Vulnerability",0,10,cp['coastal'])
            landslide=st.slider("Landslide Risk",0,10,cp['landslide'])
            watersheds=st.slider("Watershed",0,10,cp['watersheds'])
            siltation=st.slider("Siltation",0,10,cp['siltation'])
            population=st.slider("Population Density",0,10,cp['population'])
            climate_c=st.slider("Climate Change",0,10,cp['climate_change'])
            wetland=st.slider("Wetland Loss",0,10,cp['wetland_loss'])

    with cr:
        s=dict(infrastructure=infra,urbanization=urban,drainage=drainage,dams=dams,
               deforestation=deforest,encroachments=encroach,agriculture=agri,
               planning=planning,political=political,preparedness=prep,topography=topo,
               river=river,coastal=coastal,landslide=landslide,watersheds=watersheds,
               siltation=siltation,population=population,climate_change=climate_c,wetland_loss=wetland)
        prob=flood_risk(city,w,s); pct=prob*100
        heat=heat_risk(w,city); hl,hc,he=hlabel(heat)

        if pct>=65: col,label,emoji="#ef4444","HIGH RISK","🔴"
        elif pct>=40: col,label,emoji="#f59e0b","MEDIUM RISK","🟡"
        else: col,label,emoji="#10b981","LOW RISK","🟢"

        st.markdown(f"""
        <div class="pred" style="border-color:{col}">
          <div style="font-family:'Space Mono',monospace;font-size:.72rem;color:#7a8ea8">
            {city.upper()} · {datetime.now().strftime('%d %b %Y %H:%M')}
          </div>
          <div class="pred-n" style="color:{col}">{pct:.1f}%</div>
          <div style="color:{col};font-size:1.1rem;margin-top:6px">{emoji} {label}</div>
          <div style="color:#7a8ea8;font-size:.75rem;margin-top:4px">Flood Probability · Seasonal adjusted</div>
        </div>""",unsafe_allow_html=True)

        fig,ax=dfig(6,1.1)
        ax.barh([''],[40],color='#064e3b',height=.5)
        ax.barh([''],[25],color='#78350f',height=.5,left=40)
        ax.barh([''],[35],color='#7f1d1d',height=.5,left=65)
        ax.axvline(pct,color='white',lw=2.5,ls='--')
        ax.text(min(pct+2,92),0,f'{pct:.0f}%',color='white',va='center',fontsize=9,fontfamily='monospace')
        ax.set_xlim(0,100); ax.set_xticks([0,40,65,100])
        ax.set_xticklabels(['0','Low','High','100'],fontsize=8); ax.set_yticks([])
        plt.tight_layout(pad=.3); st.pyplot(fig); plt.close()

        st.markdown(f"""
        <div style="background:#0d1421;border:1px solid #1e2d45;border-radius:10px;
                    padding:14px;margin:8px 0;display:flex;justify-content:space-between">
          <div>
            <div style="font-size:.68rem;color:#7a8ea8;text-transform:uppercase;letter-spacing:.08em">Heatwave Risk</div>
            <div style="font-family:'Space Mono',monospace;font-size:1.4rem;color:{hc};font-weight:700">{heat:.0f}% {he}</div>
            <div style="font-size:.75rem;color:{hc}">{hl}</div>
          </div>
          <div style="text-align:right;font-size:.75rem;color:#7a8ea8">
            {w['temp']}°C / feels {w['feels']}°C<br>
            Humidity: {w['hum']}%<br>
            Province: {ci['province']}
          </div>
        </div>""",unsafe_allow_html=True)

        if label=="HIGH RISK":
            st.markdown(f'<div class="alert a-crit"><b>⚠️ IMMEDIATE ACTION — {city}</b><br>🚨 Issue flood warning · 🚧 Close low-lying roads<br>🏗️ Deploy pumps · 📢 Alert NDMA · 🏠 Begin evacuation</div>',unsafe_allow_html=True)
        elif label=="MEDIUM RISK":
            st.markdown(f'<div class="alert a-warn"><b>⚡ STAY ALERT — {city}</b><br>📡 Monitor rainfall · 🔍 Inspect drainage · 📋 Standby teams</div>',unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="alert a-ok"><b>✅ NORMAL — {city}</b><br>📊 Routine monitoring · 🌱 Maintain infrastructure</div>',unsafe_allow_html=True)

        if st.button("💾 Save Alert to Database",type="primary"):
            db_flood(city,prob,label,w,heat); st.success("Saved!")

# ═══════════════════════════════════════════════════════════════
# PAGE: HEATWAVE
# ═══════════════════════════════════════════════════════════════
elif "Heatwave" in page:
    st.markdown("# 🌡️ Heatwave Alert Module")
    st.markdown("Real-time temperature monitoring — Pakistan faces extreme heat (up to 54°C)")
    if season['w']: st.markdown(f'<div class="alert a-info">{season["e"]} {season["w"]}</div>',unsafe_allow_html=True)
    st.markdown("---")

    heat_data=[]
    prog=st.progress(0,"Loading city temperatures...")
    for i,(cn,_) in enumerate(CITIES.items()):
        w=get_weather(cn); hs=heat_risk(w,cn); hl,hc,he=hlabel(hs)
        heat_data.append({"city":cn,"temp":w['temp'],"feels":w['feels'],"hum":w['hum'],"score":hs,"label":hl,"color":hc,"emoji":he})
        prog.progress((i+1)/len(CITIES))
    prog.empty()
    heat_data.sort(key=lambda x:x['score'],reverse=True)

    st.markdown('<div class="sec">All Cities — Heatwave Risk Ranking</div>',unsafe_allow_html=True)
    heat_grid = '<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:10px;margin:8px 0">'
    for d in heat_data:
        bc = 'b-r' if d['score']>=70 else 'b-a' if d['score']>=50 else 'b-g'
        heat_grid += f"""
        <div class="card" style="border-color:{d['color']}40;min-width:0">
          <b style="color:#e8edf5;font-size:.88rem">{d['city']}</b><br>
          <span style="font-family:monospace;font-size:1.2rem;color:{d['color']}">{d['temp']}°C</span>
          <span style="font-size:.7rem;color:#7a8ea8"> /{d['feels']}°C</span><br>
          <div class="prog-w" style="margin:5px 0"><div class="prog-f" style="width:{d['score']}%;background:{d['color']}"></div></div>
          <span class="badge {bc}">{d['emoji']} {d['label']} {d['score']:.0f}%</span>
        </div>"""
    heat_grid += '</div>'
    st.markdown(heat_grid, unsafe_allow_html=True)

    st.markdown("---")
    cl,cr=st.columns(2)
    with cl:
        st.markdown('<div class="sec">Temperature Ranking</div>',unsafe_allow_html=True)
        fig,ax=dfig(6,7)
        sd=sorted(heat_data,key=lambda x:x['temp'])
        ax.barh([x['city'] for x in sd],[x['temp'] for x in sd],color=[x['color'] for x in sd])
        ax.axvline(45,color='#ef4444',ls='--',lw=1,label='Extreme 45°C')
        ax.axvline(40,color='#f59e0b',ls='--',lw=1,label='High 40°C')
        ax.set_xlabel('Temperature (°C)')
        ax.legend(facecolor='#0d1421',labelcolor='#7a8ea8',fontsize=8)
        ax.set_title('Live Temperatures',color='#e8edf5',fontfamily='monospace',fontsize=11)
        plt.tight_layout(); st.pyplot(fig); plt.close()
    with cr:
        st.markdown('<div class="sec">Heatwave Risk Score</div>',unsafe_allow_html=True)
        fig,ax=dfig(6,7)
        sd2=sorted(heat_data,key=lambda x:x['score'])
        ax.barh([x['city'] for x in sd2],[x['score'] for x in sd2],color=[x['color'] for x in sd2])
        ax.axvline(70,color='#ef4444',ls='--',lw=1,label='Extreme 70')
        ax.axvline(50,color='#f59e0b',ls='--',lw=1,label='High 50')
        ax.set_xlim(0,100); ax.set_xlabel('Risk Score')
        ax.legend(facecolor='#0d1421',labelcolor='#7a8ea8',fontsize=8)
        ax.set_title('Heatwave Risk Score',color='#e8edf5',fontfamily='monospace',fontsize=11)
        plt.tight_layout(); st.pyplot(fig); plt.close()

    st.markdown("---")
    st.markdown('<div class="sec">City Heatwave Detail</div>',unsafe_allow_html=True)
    sel=st.selectbox("Select City",list(CITIES.keys()))
    w=get_weather(sel); hs=heat_risk(w,sel); hl,hc,he=hlabel(hs)
    c1,c2,c3,c4=st.columns(4)
    with c1: st.metric("Temperature",f"{w['temp']}°C")
    with c2: st.metric("Feels Like",f"{w['feels']}°C")
    with c3: st.metric("Humidity",f"{w['hum']}%")
    with c4: st.metric("Risk Score",f"{hs:.0f}%",hl)
    if hl in ["EXTREME","HIGH"]:
        st.markdown(f'<div class="alert a-crit"><b>🌡️ {hl} HEATWAVE — {sel}</b><br>⚕️ Open cooling centers · 🏥 Alert hospitals · 🚰 Distribute water<br>⛔ Restrict outdoor work 11am–4pm · 👴 Prioritize vulnerable groups</div>',unsafe_allow_html=True)
    elif hl=="MODERATE":
        st.markdown(f'<div class="alert a-warn"><b>⚠️ MODERATE HEAT — {sel}</b><br>💧 Encourage hydration · 🌳 Shade recommendations · 📢 Public awareness</div>',unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="alert a-ok"><b>✅ LOW HEAT RISK — {sel}</b><br>Normal conditions. Continue routine monitoring.</div>',unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# PAGE: 7-DAY FORECAST
# ═══════════════════════════════════════════════════════════════
elif "Forecast" in page:
    st.markdown("# 📅 7-Day Forecast")
    st.markdown("AI flood + heatwave predictions using 7-day weather data from Open-Meteo")
    st.markdown("---")
    city=st.selectbox("Select City",list(CITIES.keys()))
    cp=get_sliders(city)
    with st.spinner("Fetching 7-day data..."): w=get_weather(city)

    if w['fc']:
        fc=w['fc']; days=[]
        for i in range(7):
            fw={"temp":fc['temperature_2m_max'][i],"feels":fc['temperature_2m_max'][i]+2,
                "hum":60,"precip":fc['precipitation_sum'][i],"rain":fc['precipitation_sum'][i],
                "wind":12,"rp":fc['precipitation_probability_max'][i],"code":fc['weathercode'][i],"live":True}
            days.append({"date":fc['time'][i],"tmax":fc['temperature_2m_max'][i],
                         "tmin":fc['temperature_2m_min'][i],"precip":fc['precipitation_sum'][i],
                         "rp":fc['precipitation_probability_max'][i],"code":fc['weathercode'][i],
                         "flood":flood_risk(city,fw,cp)*100,"heat":heat_risk(fw,city)})

        st.markdown('<div class="sec">7-Day Daily Cards</div>',unsafe_allow_html=True)
        # Responsive 7-day cards — scrollable on mobile
        forecast_html = '<div style="display:grid;grid-template-columns:repeat(7,minmax(90px,1fr));gap:8px;overflow-x:auto;padding-bottom:4px">'
        for d in days:
            fc2=rcol(d['flood']); _,hc2,_=hlabel(d['heat'])
            dlbl=pd.to_datetime(d['date']).strftime('%a %d')
            forecast_html += f"""
            <div style="background:#0d1421;border:1px solid #1e2d45;border-radius:10px;
                        padding:10px 6px;text-align:center;min-width:85px">
              <div style="font-family:monospace;font-size:.62rem;color:#7a8ea8">{dlbl}</div>
              <div style="font-size:1.2rem;margin:3px 0">{wemoji(d['code'])}</div>
              <div style="font-size:.82rem;color:#e8edf5;font-weight:600">{d['tmax']:.0f}°C</div>
              <div style="font-size:.65rem;color:#3d5170">{d['tmin']:.0f}°C</div>
              <div style="margin:5px 0">
                <div style="font-family:monospace;font-size:.8rem;color:{fc2};font-weight:700">{d['flood']:.0f}%</div>
                <div style="font-size:.58rem;color:#3d5170">flood</div>
              </div>
              <div>
                <div style="font-family:monospace;font-size:.8rem;color:{hc2};font-weight:700">{d['heat']:.0f}%</div>
                <div style="font-size:.58rem;color:#3d5170">heat</div>
              </div>
              <div style="font-size:.6rem;color:#3b82f6;margin-top:4px">🌧️{d['rp']:.0f}%</div>
            </div>"""
        forecast_html += '</div>'
        st.markdown(forecast_html, unsafe_allow_html=True)

        st.markdown("---")
        fig,(ax1,ax2)=plt.subplots(2,1,figsize=(11,6),sharex=True)
        fig.patch.set_facecolor('#080c14')
        for ax in [ax1,ax2]:
            ax.set_facecolor('#0d1421'); ax.tick_params(colors='#7a8ea8'); ax.spines[:].set_color('#1e2d45')
        dlabels=[pd.to_datetime(d['date']).strftime('%a %d') for d in days]
        fv=[d['flood'] for d in days]; hv=[d['heat'] for d in days]
        ax1.bar(dlabels,fv,color=[rcol(v) for v in fv],alpha=.8,width=.5)
        ax1.plot(dlabels,fv,'o-',color='white',lw=1.5,ms=4,zorder=5)
        ax1.axhline(65,color='#ef4444',ls='--',lw=1,alpha=.6)
        ax1.axhline(40,color='#f59e0b',ls='--',lw=1,alpha=.6)
        ax1.set_ylim(0,100); ax1.set_ylabel('Flood Risk %',color='#7a8ea8')
        ax1.set_title(f'7-Day Forecast — {city}',color='#e8edf5',fontfamily='monospace',fontsize=12)
        for bar,val in zip(ax1.patches,fv):
            ax1.text(bar.get_x()+bar.get_width()/2,bar.get_height()+1,f'{val:.0f}%',ha='center',color='white',fontsize=8)
        ax2.bar(dlabels,hv,color=[hlabel(v)[1] for v in hv],alpha=.8,width=.5)
        ax2.plot(dlabels,hv,'s-',color='white',lw=1.5,ms=4,zorder=5)
        ax2.axhline(70,color='#ef4444',ls='--',lw=1,alpha=.6)
        ax2.axhline(50,color='#f59e0b',ls='--',lw=1,alpha=.6)
        ax2.set_ylim(0,100); ax2.set_ylabel('Heat Risk %',color='#7a8ea8')
        plt.tight_layout(); st.pyplot(fig); plt.close()

        peak=max(days,key=lambda x:x['flood'])
        if peak['flood']>=40:
            pc=rcol(peak['flood'])
            st.markdown(f'<div class="alert a-warn"><b>⚠️ Peak Flood Risk: {pd.to_datetime(peak["date"]).strftime("%A %d %b")}</b> — {peak["flood"]:.0f}% with {peak["precip"]:.1f}mm rainfall and {peak["rp"]:.0f}% rain chance.</div>',unsafe_allow_html=True)
        st.download_button("📥 Download Forecast CSV",pd.DataFrame(days).to_csv(index=False),f"{city}_forecast.csv","text/csv")
    else:
        st.warning("Could not fetch forecast. Check internet connection.")

# ═══════════════════════════════════════════════════════════════
# PAGE: RISK MAP
# ═══════════════════════════════════════════════════════════════
elif "Map" in page:
    try:
        import folium
        from streamlit_folium import st_folium
        st.markdown("# 🗺️ Pakistan Risk Map")
        st.markdown("Interactive flood and heatwave risk — click any bubble for full details")
        st.markdown("---")
        c1,c2,c3=st.columns(3)
        with c1: rt=st.selectbox("Show Risk",["Flood Risk","Heatwave Risk","Combined"])
        with c2: rf=st.selectbox("Filter",["All","Very High (≥70%)","High (40-70%)","Low (<40%)"])
        with c3: mt=st.selectbox("Map Style",["CartoDB dark_matter","OpenStreetMap","CartoDB positron"])
        m=folium.Map(location=[29.5,69.5],zoom_start=6,tiles=mt)
        tdata=[]; pg=st.progress(0,"Fetching city data...")
        for idx,(cn,ci) in enumerate(CITIES.items()):
            w=get_weather(cn); fr=flood_risk(cn,w)*100; hr=heat_risk(w,cn)
            sc=(fr+hr)/2 if rt=="Combined" else fr if rt=="Flood Risk" else hr
            col=rcol(sc)
            skip=False
            if rf=="Very High (≥70%)" and sc<70: skip=True
            if rf=="High (40-70%)" and not(40<=sc<70): skip=True
            if rf=="Low (<40%)" and sc>=40: skip=True
            if not skip:
                ph=f"""<div style="font-family:sans-serif;min-width:220px;background:#0d1421;color:#e8edf5;padding:14px;border-radius:8px;border:1px solid {col}">
                <h4 style="color:{col};margin:0 0 6px">{cn}</h4>
                <b style="font-size:1.2rem;color:{col}">{sc:.1f}%</b> {rt}<br>
                <hr style="border-color:#1e2d45;margin:7px 0">
                Province: {ci['province']} · Pop: {ci['pop']}<br>
                🌊 Flood: {fr:.1f}% · 🌡️ Heat: {hr:.1f}%<br>
                Temp: {w['temp']}°C · Humidity: {w['hum']}%<br>
                <span style="color:#7a8ea8;font-size:.8rem">{ci['reason'][:60]}</span></div>"""
                folium.CircleMarker(location=[ci['lat'],ci['lon']],radius=int(6+sc/8),
                    color=col,fill=True,fill_color=col,fill_opacity=.75,
                    popup=folium.Popup(folium.IFrame(ph,width=240,height=210),max_width=250),
                    tooltip=f"{cn}: {sc:.0f}%").add_to(m)
            tdata.append({"City":cn,"Province":ci['province'],"Flood %":round(fr,1),
                          "Heat %":round(hr,1),"Temp °C":w['temp'],"Rain %":w['rp'],"Why":ci['reason'][:55]})
            pg.progress((idx+1)/len(CITIES))
        pg.empty()
        legend="""<div style="position:fixed;bottom:25px;left:25px;z-index:9999;background:rgba(13,20,33,.95);
                   border:1px solid #1e2d45;border-radius:8px;padding:12px;font-family:monospace;font-size:.75rem">
                   <b style="color:#e8edf5">Risk Level</b><br>
                   <span style="color:#ef4444">⬤ Very High ≥70%</span><br>
                   <span style="color:#f59e0b">⬤ High 40-70%</span><br>
                   <span style="color:#10b981">⬤ Low &lt;40%</span></div>"""
        m.get_root().html.add_child(folium.Element(legend))
        st_folium(m,width=None,height=570,returned_objects=[])
        st.markdown("---")
        df_t=pd.DataFrame(tdata).sort_values("Flood %",ascending=False)
        st.dataframe(df_t,use_container_width=True,hide_index=True)
        st.download_button("📥 Download CSV",df_t.to_csv(index=False),"risk_map.csv","text/csv")
    except ImportError:
        st.error("Run: pip install folium streamlit-folium")

# ═══════════════════════════════════════════════════════════════
# PAGE: WASTE MONITOR
# ═══════════════════════════════════════════════════════════════
elif "Waste" in page:
    st.markdown("# 🗑️ Smart Waste Management")
    st.markdown("RandomForest model · R²=0.9998 · MAE=0.19% · Real-time bin monitoring")
    st.markdown("---")
    tab1,tab2=st.tabs(["📊 Live Monitor","🤖 Predict Collection"])

    with tab1:
        latest=WDF.sort_values('timestamp').groupby('bin_id').last().reset_index()
        c1,c2,c3,c4=st.columns(4)
        with c1: st.metric("Total Bins",len(latest))
        with c2: st.metric("Critical ≥85%",(latest['fill_level_%']>=85).sum(),"Collect now")
        with c3: st.metric("High 70-85%",((latest['fill_level_%']>=70)&(latest['fill_level_%']<85)).sum())
        with c4: st.metric("Avg Fill",f"{latest['fill_level_%'].mean():.1f}%")

        st.markdown('<div class="sec">Bin Status — All Units</div>',unsafe_allow_html=True)
        for _,row in latest.sort_values('fill_level_%',ascending=False).iterrows():
            fill=row['fill_level_%']
            if fill>=85:   css,status="a-crit","🔴 CRITICAL — Immediate collection required"
            elif fill>=70: css,status="a-warn","🟠 HIGH — Schedule collection soon"
            else:          css,status="a-ok","🟢 OK — Within normal range"
            bar="█"*int(fill/5)+"░"*(20-int(fill/5))
            st.markdown(f"""
            <div class="alert {css}">
              <div style="display:flex;justify-content:space-between">
                <div><b>{row['bin_id']}</b> — {row['area']} <span class="badge b-b">{row['bin_type']}</span></div>
                <b style="font-family:'Space Mono',monospace">{fill:.1f}%</b>
              </div>
              <div style="font-family:'Space Mono',monospace;font-size:.78rem;margin:3px 0;letter-spacing:.04em">{bar}</div>
              <div style="font-size:.76rem">{status}</div>
            </div>""",unsafe_allow_html=True)

        st.markdown('<div class="sec">Fill Level Trend</div>',unsafe_allow_html=True)
        sb=st.selectbox("Select bin",WDF['bin_id'].unique())
        bd=WDF[WDF['bin_id']==sb].tail(42)
        fig,ax=dfig(10,3.5)
        ax.plot(bd['timestamp'],bd['fill_level_%'],color='#3b82f6',lw=2)
        ax.fill_between(bd['timestamp'],bd['fill_level_%'],alpha=.15,color='#3b82f6')
        ax.axhline(85,color='#ef4444',ls='--',lw=1.5,label='Critical 85%')
        ax.axhline(70,color='#f59e0b',ls='--',lw=1.5,label='High 70%')
        ax.set_ylabel('Fill Level (%)'); ax.set_ylim(0,105)
        ax.legend(facecolor='#0d1421',labelcolor='#7a8ea8')
        ax.set_title(f'Fill Trend — {sb}',color='#e8edf5',fontfamily='monospace')
        plt.xticks(rotation=35); plt.tight_layout(); st.pyplot(fig); plt.close()

    with tab2:
        c1,c2=st.columns(2)
        with c1:
            bid=st.selectbox("Bin ID",WDF['bin_id'].unique())
            btype=st.selectbox("Bin Type",["General","Recyclable","Organic"])
            pf=st.slider("Current Fill (%)",0.0,100.0,68.0)
            fc_chg=st.slider("Fill Change (last reading)",-5.0,20.0,7.5)
            tw=st.slider("Temperature (°C)",25.0,48.0,36.0)
            hw=st.slider("Humidity (%)",40.0,95.0,70.0)
        with c2:
            hr2=st.slider("Hour of Day",0,23,14)
            dy=st.selectbox("Day",["Mon","Tue","Wed","Thu","Fri","Sat","Sun"])
            mo=st.slider("Month",1,12,5)
            dm={"Mon":0,"Tue":1,"Wed":2,"Thu":3,"Fri":4,"Sat":5,"Sun":6}
            tm={"General":0,"Recyclable":1,"Organic":2}
            iw=1 if dm[dy]>=5 else 0
            samp=pd.DataFrame([{'prev_fill_level':pf,'fill_change':fc_chg,'hour':hr2,
                'day_of_week':dm[dy],'month':mo,'is_weekend':iw,
                'temperature_C':tw,'humidity_%':hw,'bin_type_code':tm[btype]}])
            pc2=int(WC.predict(samp)[0]); pf2=float(np.clip(WR.predict(samp)[0],0,100))
            col2="#ef4444" if pc2==1 else "#10b981"
            msg2="COLLECTION NEEDED" if pc2==1 else "NO COLLECTION YET"
            ic2="🚛" if pc2==1 else "✅"
            st.markdown(f"""
            <div class="pred" style="border-color:{col2};margin-top:16px">
              <div style="font-size:2.2rem">{ic2}</div>
              <div style="font-family:'Space Mono',monospace;font-size:1.1rem;color:{col2};font-weight:700;margin-top:6px">{msg2}</div>
              <div style="color:#7a8ea8;margin-top:8px;font-size:.82rem">Next predicted fill level:<br>
                <b style="font-family:'Space Mono',monospace;font-size:1.3rem;color:{col2}">{pf2:.1f}%</b>
              </div>
            </div>""",unsafe_allow_html=True)
            ar=WDF[WDF['bin_id']==bid]['area'].iloc[0] if bid in WDF['bin_id'].values else btype
            if st.button("💾 Save to Database",type="primary"):
                db_waste(bid,ar,pf2,pc2); st.success("Saved!")

# ═══════════════════════════════════════════════════════════════
# PAGE: ROUTE OPTIMIZER
# ═══════════════════════════════════════════════════════════════
elif "Route" in page:
    st.markdown("# 🚛 Waste Collection Route Optimizer")
    st.markdown("Nearest-neighbor TSP heuristic — minimizes truck travel distance for collection runs")
    st.markdown("---")
    latest=WDF.sort_values('timestamp').groupby('bin_id').last().reset_index()
    np.random.seed(42); n=len(latest)
    base_lat,base_lon=31.55,74.35
    latest['latitude'] =base_lat+np.random.uniform(-0.08,0.08,n)
    latest['longitude']=base_lon+np.random.uniform(-0.08,0.08,n)

    c1,c2,c3=st.columns(3)
    with c1: thr=st.slider("Collection threshold (%)",50,90,75)
    with c2: st.metric("Total Bins",len(latest))
    with c3: st.metric("Bins to Collect",(latest['fill_level_%']>=thr).sum(),f"≥{thr}%")

    latest['collection_needed']=(latest['fill_level_%']>=thr).astype(int)
    route,total_km=optimize_route(latest)

    if route:
        c1,c2,c3,c4=st.columns(4)
        with c1: st.metric("Stops in Route",len(route))
        with c2: st.metric("Total Distance",f"{total_km:.2f} km")
        with c3: st.metric("Est. Time",f"{int(total_km*3)} min","@ 20 km/h")
        with c4: st.metric("Bins Skipped",len(latest)-len(route),"Below threshold")

        rrows=[{"Stop":i+1,"Bin ID":b['bin_id'],"Area":b['area'],"Type":b['bin_type'],
                "Fill Level":f"{b['fill_level_%']:.1f}%",
                "Priority":"🔴 CRITICAL" if b['fill_level_%']>=85 else "🟠 HIGH" if b['fill_level_%']>=70 else "🟡 MEDIUM"}
               for i,b in enumerate(route)]
        st.dataframe(pd.DataFrame(rrows),use_container_width=True,hide_index=True)

        try:
            import folium
            from streamlit_folium import st_folium
            st.markdown('<div class="sec">Route Map</div>',unsafe_allow_html=True)
            rm=folium.Map(location=[base_lat,base_lon],zoom_start=13,tiles="CartoDB dark_matter")
            for _,row in latest.iterrows():
                fill=row['fill_level_%']
                col3="#ef4444" if fill>=85 else "#f59e0b" if fill>=70 else "#10b981"
                folium.CircleMarker(location=[row['latitude'],row['longitude']],radius=5,
                    color=col3,fill=True,fill_color=col3,fill_opacity=.8,
                    tooltip=f"{row['bin_id']}: {fill:.1f}%").add_to(rm)
            folium.PolyLine([[b['latitude'],b['longitude']] for b in route],
                color="#3b82f6",weight=3,opacity=.8,dash_array="5 5").add_to(rm)
            for i,b in enumerate(route):
                folium.Marker(location=[b['latitude'],b['longitude']],
                    icon=folium.DivIcon(
                        html=f'<div style="background:#3b82f6;color:white;border-radius:50%;width:20px;height:20px;text-align:center;font-size:11px;font-weight:700;line-height:20px;font-family:monospace">{i+1}</div>',
                        icon_size=(20,20))).add_to(rm)
            st_folium(rm,width=None,height=430,returned_objects=[])
        except ImportError:
            st.info("pip install folium streamlit-folium for route map")

        st.download_button("📥 Download Route Plan",pd.DataFrame(rrows).to_csv(index=False),"route.csv","text/csv")
    else:
        st.success(f"✅ No bins above {thr}% — no collection run needed!")

# ═══════════════════════════════════════════════════════════════
# PAGE: MODEL PERFORMANCE
# ═══════════════════════════════════════════════════════════════
elif "Performance" in page:
    st.markdown("# 📊 Model Performance Metrics")
    st.markdown("Evaluation report — accuracy, precision, recall, F1, MAE, R² for both models")
    st.markdown("---")
    tab1,tab2=st.tabs(["🌊 Flood Model","🗑️ Waste Model"])

    with tab1:
        st.markdown('<div class="sec">Flood Prediction — GradientBoostingRegressor</div>',unsafe_allow_html=True)
        c1,c2,c3,c4=st.columns(4)
        with c1: st.metric("R² Score","0.9920","Test set")
        with c2: st.metric("MAE","0.0033","Very low error")
        with c3: st.metric("n_estimators","200")
        with c4: st.metric("Features","25","20 raw + 5 engineered")

        st.markdown('<div class="sec">Feature Importance</div>',unsafe_allow_html=True)
        feats=['Total_Risk_Score','TopographyDrainage','PopulationScore','Watersheds',
               'CoastalVulnerability','RiverManagement','Landslides','Siltation',
               'Human_Activity_Risk','AgriculturalPractices']
        imps=[0.630,0.052,0.051,0.050,0.050,0.048,0.047,0.045,0.022,0.010]
        fig,ax=dfig(8,4)
        fc3=['#3b82f6' if i==0 else '#1e3a5f' for i in range(len(feats))]
        ax.barh(feats[::-1],imps[::-1],color=fc3[::-1])
        ax.set_xlabel('Importance Score')
        for i,v in enumerate(imps[::-1]): ax.text(v+.002,i,f'{v:.3f}',va='center',color='#7a8ea8',fontsize=8)
        ax.set_title('Feature Importance — Flood Model',color='#e8edf5',fontfamily='monospace',fontsize=11)
        plt.tight_layout(); st.pyplot(fig); plt.close()

        st.markdown('<div class="sec">Training Config</div>',unsafe_allow_html=True)
        st.dataframe(pd.DataFrame({
            "Parameter":["Algorithm","n_estimators","learning_rate","max_depth",
                         "Train/Test Split","Training Samples","R² Train","R² Test","MAE Test"],
            "Value":["GradientBoostingRegressor","200","0.05","5",
                     "80% / 20%","~40,000","0.9941","0.9920","0.0033"]
        }),use_container_width=True,hide_index=True)

        st.markdown("""<div class="alert a-info">
        <b>Key Insight:</b> <b>Total_Risk_Score</b> (63% importance) is our engineered feature combining 
        all four risk groups. This single feature captures the combined effect of infrastructure, human activity, 
        climate, and governance risk — explaining why feature engineering boosted R² from 0.56 to 0.99.
        </div>""",unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="sec">Waste Classification — RandomForestClassifier</div>',unsafe_allow_html=True)
        c1,c2,c3,c4=st.columns(4)
        with c1: st.metric("Accuracy","~99%","Classification")
        with c2: st.metric("Precision","~98%","Collection needed")
        with c3: st.metric("Recall","~99%","Collection needed")
        with c4: st.metric("F1 Score","~98.5%","Weighted avg")

        st.markdown('<div class="sec">Waste Regressor — RandomForestRegressor</div>',unsafe_allow_html=True)
        c1,c2,c3,c4=st.columns(4)
        with c1: st.metric("R² Score","0.9998","Near perfect")
        with c2: st.metric("MAE","0.19%","Fill level error")
        with c3: st.metric("n_estimators","100")
        with c4: st.metric("Features","9","Sensor + time")

        st.markdown('<div class="sec">Feature Importance — Waste Model</div>',unsafe_allow_html=True)
        wf=['prev_fill_level','fill_change','humidity_%','temperature_C',
            'is_weekend','hour','day_of_week','month','bin_type_code']
        wi=[0.859,0.086,0.014,0.013,0.010,0.008,0.006,0.003,0.001]
        fig,ax=dfig(8,3.5)
        wc2=['#10b981' if i==0 else '#064e3b' for i in range(len(wf))]
        ax.barh(wf[::-1],wi[::-1],color=wc2[::-1])
        ax.set_xlabel('Importance Score')
        ax.set_title('Feature Importance — Waste Model',color='#e8edf5',fontfamily='monospace',fontsize=11)
        plt.tight_layout(); st.pyplot(fig); plt.close()

        st.markdown("""<div class="alert a-info">
        <b>Key Insight:</b> <b>prev_fill_level</b> (85.9%) dominates — the current fill level is the 
        strongest predictor of whether collection is needed. This makes physical sense. 
        <b>fill_change</b> (8.6%) captures the rate of filling. Environmental factors 
        (humidity, temperature) have minor but measurable effects on organic waste expansion.
        </div>""",unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# PAGE: ALERT HISTORY
# ═══════════════════════════════════════════════════════════════
elif "History" in page:
    st.markdown("# 🗄️ Alert History")
    st.markdown("All predictions and alerts saved to SQLite database — exportable as CSV")
    st.markdown("---")
    tab1,tab2=st.tabs(["🌊 Flood & Heat Alerts","🗑️ Waste Alerts"])
    with tab1:
        df=db_get("flood_alerts")
        if df.empty: st.info("No alerts yet — go to Flood Prediction and save a prediction.")
        else:
            c1,c2,c3=st.columns(3)
            with c1: st.metric("Total Alerts",len(df))
            with c2: st.metric("Cities",df['city'].nunique() if 'city' in df.columns else 0)
            with c3: st.metric("High Risk",(df['risk']=="HIGH RISK").sum() if 'risk' in df.columns else 0)
            st.dataframe(df,use_container_width=True,hide_index=True)
            st.download_button("📥 Download CSV",df.to_csv(index=False),"flood_alerts.csv","text/csv")
    with tab2:
        df=db_get("waste_alerts")
        if df.empty: st.info("No alerts yet — go to Waste Management and save a prediction.")
        else:
            st.metric("Total Alerts",len(df))
            st.dataframe(df,use_container_width=True,hide_index=True)
            st.download_button("📥 Download CSV",df.to_csv(index=False),"waste_alerts.csv","text/csv")


# ═══════════════════════════════════════════════════════════════
# PAGE: EMAIL ALERTS
# ═══════════════════════════════════════════════════════════════
elif "Email" in page:
    st.markdown("# 📧 Email Alert System")
    st.markdown("Auto-send alerts when flood or heatwave risk crosses critical threshold")
    st.markdown("---")

    def send_alert_email(sender, password, recipient, city, flood_pct, heat_pct, weather):
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            msg = MIMEMultipart("alternative")
            msg['Subject'] = f"⚠️ Urban AI Alert — {city} Risk Warning"
            msg['From']    = sender
            msg['To']      = recipient

            flood_color = "#ef4444" if flood_pct>=65 else "#f59e0b" if flood_pct>=40 else "#10b981"
            heat_color  = "#ef4444" if heat_pct>=70  else "#f59e0b" if heat_pct>=50  else "#10b981"

            html = f"""
            <html><body style="font-family:Arial;background:#080c14;color:#e8edf5;padding:24px">
            <div style="max-width:600px;margin:auto;background:#0d1421;border:1px solid #1e2d45;border-radius:16px;padding:28px">
                <h1 style="font-family:monospace;color:#3b82f6;margin:0 0 4px">🏙️ Urban AI System</h1>
                <p style="color:#7a8ea8;margin:0 0 20px;font-size:.85rem">GCUF · AI-Driven Urban Management · Pakistan</p>
                <hr style="border-color:#1e2d45;margin:16px 0">
                <h2 style="color:#ef4444;margin:0 0 16px">⚠️ Risk Alert — {city}</h2>
                <div style="display:flex;gap:16px;margin-bottom:20px">
                    <div style="flex:1;background:#111b2e;border:1px solid {flood_color};border-radius:10px;padding:16px;text-align:center">
                        <div style="font-size:.75rem;color:#7a8ea8;text-transform:uppercase;letter-spacing:.08em">Flood Risk</div>
                        <div style="font-family:monospace;font-size:2rem;font-weight:700;color:{flood_color}">{flood_pct:.1f}%</div>
                    </div>
                    <div style="flex:1;background:#111b2e;border:1px solid {heat_color};border-radius:10px;padding:16px;text-align:center">
                        <div style="font-size:.75rem;color:#7a8ea8;text-transform:uppercase;letter-spacing:.08em">Heat Risk</div>
                        <div style="font-family:monospace;font-size:2rem;font-weight:700;color:{heat_color}">{heat_pct:.1f}%</div>
                    </div>
                </div>
                <div style="background:#111b2e;border-radius:10px;padding:16px;margin-bottom:20px">
                    <b style="color:#3b82f6">📡 Current Weather Conditions</b><br><br>
                    🌡️ Temperature: <b>{weather['temp']}°C</b> (feels {weather['feels']}°C)<br>
                    💧 Humidity: <b>{weather['hum']}%</b><br>
                    🌧️ Rain Probability: <b>{weather['rp']}%</b><br>
                    🌡️ Precipitation: <b>{weather['precip']} mm</b>
                </div>
                <div style="background:#1a0a0a;border:1px solid #ef4444;border-radius:10px;padding:16px;margin-bottom:20px">
                    <b style="color:#ef4444">⚠️ Recommended Actions</b><br><br>
                    {"🚨 Issue public flood warning<br>🚧 Close low-lying roads<br>🏗️ Deploy emergency pumps<br>📢 Alert NDMA disaster teams" if flood_pct>=65 else "📡 Monitor rainfall closely<br>🔍 Inspect drainage systems<br>📋 Put emergency teams on standby"}
                </div>
                <p style="color:#3d5170;font-size:.75rem;text-align:center;margin:0">
                    Generated by Urban AI Management System · {datetime.now().strftime('%d %b %Y %H:%M')} · GCUF BSDS 2026
                </p>
            </div></body></html>"""

            msg.attach(MIMEText(html, "html"))
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())
            server.quit()
            return True, "Email sent successfully!"
        except Exception as ex:
            return False, str(ex)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="sec">Gmail Configuration</div>', unsafe_allow_html=True)
        st.markdown("""<div class="alert a-info">
        <b>How to set up Gmail:</b><br>
        1. Go to Google Account → Security<br>
        2. Enable 2-Step Verification<br>
        3. Go to App Passwords → Generate new<br>
        4. Use that 16-digit password below (NOT your normal password)
        </div>""", unsafe_allow_html=True)

        sender_email    = st.text_input("Your Gmail address", placeholder="yourname@gmail.com")
        sender_password = st.text_input("Gmail App Password (16 digits)", type="password", placeholder="xxxx xxxx xxxx xxxx")
        recipient_email = st.text_input("Send alerts to", placeholder="supervisor@gcuf.edu.pk")

        st.markdown('<div class="sec">Alert Settings</div>', unsafe_allow_html=True)
        alert_city       = st.selectbox("Monitor City", list(CITIES.keys()))
        flood_threshold  = st.slider("Send alert when flood risk exceeds (%)", 30, 90, 60)
        heat_threshold   = st.slider("Send alert when heat risk exceeds (%)", 30, 90, 65)

    with col2:
        st.markdown('<div class="sec">Current Risk — Selected City</div>', unsafe_allow_html=True)
        with st.spinner(f"Fetching live data for {alert_city}..."):
            w_alert = get_weather(alert_city)
        fr_alert = flood_risk(alert_city, w_alert) * 100
        hr_alert = heat_risk(w_alert, alert_city)
        fc = rcol(fr_alert); hl_a, hc_a, he_a = hlabel(hr_alert)

        st.markdown(f"""
        <div class="card">
            <b style="color:#3b82f6">{alert_city} — Live Status</b><br><br>
            <div style="display:flex;gap:12px;margin-top:8px">
                <div style="flex:1;text-align:center;background:#111b2e;border:1px solid {fc};border-radius:8px;padding:12px">
                    <div style="font-size:.7rem;color:#7a8ea8">Flood Risk</div>
                    <div style="font-family:'Space Mono',monospace;font-size:1.6rem;color:{fc};font-weight:700">{fr_alert:.1f}%</div>
                    <div style="font-size:.7rem;color:{fc}">{"⚠️ ABOVE THRESHOLD" if fr_alert>=flood_threshold else "✅ Below threshold"}</div>
                </div>
                <div style="flex:1;text-align:center;background:#111b2e;border:1px solid {hc_a};border-radius:8px;padding:12px">
                    <div style="font-size:.7rem;color:#7a8ea8">Heat Risk</div>
                    <div style="font-family:'Space Mono',monospace;font-size:1.6rem;color:{hc_a};font-weight:700">{hr_alert:.1f}%</div>
                    <div style="font-size:.7rem;color:{hc_a}">{"⚠️ ABOVE THRESHOLD" if hr_alert>=heat_threshold else "✅ Below threshold"}</div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

        c1t, c2t = st.columns(2)
        with c1t:
            if st.button("🧪 Send Test Email", type="primary"):
                if not sender_email or not sender_password or not recipient_email:
                    st.error("Please fill in all email fields first!")
                else:
                    with st.spinner("Sending..."):
                        ok, msg_result = send_alert_email(
                            sender_email, sender_password, recipient_email,
                            alert_city, fr_alert, hr_alert, w_alert)
                    if ok: st.success(f"✅ {msg_result}")
                    else:  st.error(f"❌ Failed: {msg_result}")

        with c2t:
            if st.button("🚨 Send Real Alert"):
                if fr_alert < flood_threshold and hr_alert < heat_threshold:
                    st.info(f"Risk is below your thresholds ({flood_threshold}% flood, {heat_threshold}% heat). No alert needed.")
                elif not sender_email or not sender_password or not recipient_email:
                    st.error("Fill in email settings first!")
                else:
                    with st.spinner("Sending alert..."):
                        ok, msg_result = send_alert_email(
                            sender_email, sender_password, recipient_email,
                            alert_city, fr_alert, hr_alert, w_alert)
                    if ok: st.success(f"✅ Alert sent to {recipient_email}!")
                    else:  st.error(f"❌ {msg_result}")

        st.markdown("""<div class="alert a-info" style="margin-top:12px">
        <b>💡 For your FYP viva:</b><br>
        During your demo, set threshold to 1% and click Send Real Alert —
        your supervisor will receive a professional HTML email live during the presentation!
        </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# PAGE: PDF REPORT
# ═══════════════════════════════════════════════════════════════
elif "Report" in page:
    st.markdown("# 📄 PDF Report Generator")
    st.markdown("Generate a professional city risk report — downloadable as PDF")
    st.markdown("---")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('<div class="sec">Report Configuration</div>', unsafe_allow_html=True)
        report_city    = st.selectbox("Select City", list(CITIES.keys()))
        include_flood  = st.checkbox("Include Flood Analysis", value=True)
        include_heat   = st.checkbox("Include Heatwave Analysis", value=True)
        include_waste  = st.checkbox("Include Waste Management Summary", value=True)
        include_rec    = st.checkbox("Include Recommendations", value=True)
        report_author  = st.text_input("Report prepared by", value="Urban AI Management System")

    with col2:
        st.markdown('<div class="sec">Live Data Preview</div>', unsafe_allow_html=True)
        with st.spinner("Fetching live data..."):
            w_rep  = get_weather(report_city)
        fr_rep = flood_risk(report_city, w_rep) * 100
        hr_rep = heat_risk(w_rep, report_city)
        hl_rep, hc_rep, he_rep = hlabel(hr_rep)
        ci_rep = CITIES[report_city]
        latest_rep = WDF.sort_values('timestamp').groupby('bin_id').last().reset_index()

        st.markdown(f"""
        <div class="card">
            <b style="color:#3b82f6">Report Preview — {report_city}</b><br><br>
            🌊 Flood Risk: <b style="color:{rcol(fr_rep)}">{fr_rep:.1f}%</b><br>
            🌡️ Heat Risk: <b style="color:{hc_rep}">{hr_rep:.1f}% {he_rep} {hl_rep}</b><br>
            🌡️ Temperature: <b>{w_rep['temp']}°C</b> / feels {w_rep['feels']}°C<br>
            💧 Humidity: <b>{w_rep['hum']}%</b><br>
            🗑️ Critical Bins: <b>{(latest_rep['fill_level_%']>=85).sum()}</b><br>
            📍 Province: <b>{ci_rep['province']}</b><br>
            👥 Population: <b>{ci_rep['pop']}</b><br>
            📅 Generated: <b>{datetime.now().strftime('%d %b %Y %H:%M')}</b>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    if st.button("📄 Generate PDF Report", type="primary"):
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch, cm
            from reportlab.lib import colors
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
            from reportlab.lib.enums import TA_CENTER, TA_LEFT
            import io

            buffer = io.BytesIO()
            doc    = SimpleDocTemplate(buffer, pagesize=A4,
                                       topMargin=1.5*cm, bottomMargin=1.5*cm,
                                       leftMargin=2*cm, rightMargin=2*cm)

            # Colors
            DARK  = colors.HexColor('#080c14')
            CARD  = colors.HexColor('#0d1421')
            BLUE  = colors.HexColor('#3b82f6')
            GREEN = colors.HexColor('#10b981')
            RED   = colors.HexColor('#ef4444')
            AMBER = colors.HexColor('#f59e0b')
            LIGHT = colors.HexColor('#e8edf5')
            GREY  = colors.HexColor('#7a8ea8')
            risk_col = RED if fr_rep>=65 else AMBER if fr_rep>=40 else GREEN

            styles = getSampleStyleSheet()
            title_style   = ParagraphStyle('title',   fontSize=20, textColor=BLUE,   spaceAfter=6,  fontName='Helvetica-Bold')
            sub_style     = ParagraphStyle('sub',     fontSize=10, textColor=GREY,   spaceAfter=12, fontName='Helvetica')
            heading_style = ParagraphStyle('heading', fontSize=13, textColor=BLUE,   spaceAfter=6,  fontName='Helvetica-Bold', spaceBefore=14)
            body_style    = ParagraphStyle('body',    fontSize=10, textColor=LIGHT,  spaceAfter=4,  fontName='Helvetica',      leading=16)
            bold_style    = ParagraphStyle('bold',    fontSize=10, textColor=LIGHT,  spaceAfter=4,  fontName='Helvetica-Bold')

            story = []

            # Header
            story.append(Paragraph("AI-DRIVEN URBAN MANAGEMENT SYSTEM", title_style))
            story.append(Paragraph(f"City Risk Assessment Report — {report_city}", sub_style))
            story.append(Paragraph(f"Generated: {datetime.now().strftime('%d %B %Y at %H:%M')} | Prepared by: {report_author}", sub_style))
            story.append(HRFlowable(width="100%", thickness=1, color=BLUE, spaceAfter=12))

            # City overview table
            story.append(Paragraph("CITY OVERVIEW", heading_style))
            overview_data = [
                ["Parameter", "Value"],
                ["City", report_city],
                ["Province", ci_rep['province']],
                ["Population", ci_rep['pop']],
                ["Coastal City", "Yes" if ci_rep['coastal'] else "No"],
                ["Season", get_season()['name']],
                ["Report Date", datetime.now().strftime('%d %B %Y')],
            ]
            t = Table(overview_data, colWidths=[5*cm, 10*cm])
            t.setStyle(TableStyle([
                ('BACKGROUND',  (0,0), (-1,0), BLUE),
                ('TEXTCOLOR',   (0,0), (-1,0), colors.white),
                ('FONTNAME',    (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE',    (0,0), (-1,-1), 10),
                ('BACKGROUND',  (0,1), (-1,-1), CARD),
                ('TEXTCOLOR',   (0,1), (-1,-1), LIGHT),
                ('ROWBACKGROUNDS',(0,1),(-1,-1),[CARD, colors.HexColor('#111b2e')]),
                ('GRID',        (0,0), (-1,-1), 0.5, colors.HexColor('#1e2d45')),
                ('PADDING',     (0,0), (-1,-1), 8),
            ]))
            story.append(t)
            story.append(Spacer(1, 12))

            if include_flood:
                story.append(Paragraph("FLOOD RISK ANALYSIS", heading_style))
                flood_level = "HIGH RISK" if fr_rep>=65 else "MEDIUM RISK" if fr_rep>=40 else "LOW RISK"
                flood_data = [
                    ["Metric", "Value", "Status"],
                    ["Flood Probability", f"{fr_rep:.1f}%", flood_level],
                    ["Temperature",       f"{w_rep['temp']}°C",  "Live data"],
                    ["Feels Like",        f"{w_rep['feels']}°C", "Live data"],
                    ["Humidity",          f"{w_rep['hum']}%",    "Live data"],
                    ["Rain Probability",  f"{w_rep['rp']}%",     "Next 6 hours"],
                    ["Precipitation",     f"{w_rep['precip']} mm","Current"],
                    ["Model Accuracy",    "R² = 0.9920",         "GradientBoosting"],
                ]
                t2 = Table(flood_data, colWidths=[5*cm, 5*cm, 5*cm])
                t2.setStyle(TableStyle([
                    ('BACKGROUND',  (0,0), (-1,0), BLUE),
                    ('TEXTCOLOR',   (0,0), (-1,0), colors.white),
                    ('FONTNAME',    (0,0), (-1,0), 'Helvetica-Bold'),
                    ('FONTSIZE',    (0,0), (-1,-1), 10),
                    ('BACKGROUND',  (2,1), (2,1), RED if fr_rep>=65 else AMBER if fr_rep>=40 else GREEN),
                    ('ROWBACKGROUNDS',(0,1),(-1,-1),[CARD, colors.HexColor('#111b2e')]),
                    ('TEXTCOLOR',   (0,1), (-1,-1), LIGHT),
                    ('GRID',        (0,0), (-1,-1), 0.5, colors.HexColor('#1e2d45')),
                    ('PADDING',     (0,0), (-1,-1), 8),
                ]))
                story.append(t2)
                story.append(Spacer(1, 8))

            if include_heat:
                story.append(Paragraph("HEATWAVE RISK ANALYSIS", heading_style))
                heat_data_pdf = [
                    ["Metric", "Value", "Status"],
                    ["Heatwave Risk Score", f"{hr_rep:.1f}%", hl_rep],
                    ["Current Temperature", f"{w_rep['temp']}°C", "Live data"],
                    ["Feels Like Temp",     f"{w_rep['feels']}°C","Live data"],
                    ["Humidity",            f"{w_rep['hum']}%",   "Live data"],
                    ["Jacobabad Note", "Hottest city", "Extreme risk zone" if report_city=="Jacobabad" else "N/A"],
                ]
                t3 = Table(heat_data_pdf, colWidths=[5*cm, 5*cm, 5*cm])
                t3.setStyle(TableStyle([
                    ('BACKGROUND',  (0,0), (-1,0), BLUE),
                    ('TEXTCOLOR',   (0,0), (-1,0), colors.white),
                    ('FONTNAME',    (0,0), (-1,0), 'Helvetica-Bold'),
                    ('FONTSIZE',    (0,0), (-1,-1), 10),
                    ('ROWBACKGROUNDS',(0,1),(-1,-1),[CARD, colors.HexColor('#111b2e')]),
                    ('TEXTCOLOR',   (0,1), (-1,-1), LIGHT),
                    ('GRID',        (0,0), (-1,-1), 0.5, colors.HexColor('#1e2d45')),
                    ('PADDING',     (0,0), (-1,-1), 8),
                ]))
                story.append(t3)
                story.append(Spacer(1, 8))

            if include_waste:
                story.append(Paragraph("WASTE MANAGEMENT SUMMARY", heading_style))
                latest_w = WDF.sort_values('timestamp').groupby('bin_id').last().reset_index()
                waste_data_pdf = [
                    ["Metric", "Value"],
                    ["Total Bins Monitored",  str(len(latest_w))],
                    ["Critical Bins (≥85%)",  str((latest_w['fill_level_%']>=85).sum())],
                    ["High Bins (70-85%)",    str(((latest_w['fill_level_%']>=70)&(latest_w['fill_level_%']<85)).sum())],
                    ["Average Fill Level",    f"{latest_w['fill_level_%'].mean():.1f}%"],
                    ["Model Accuracy",        "R² = 0.9998"],
                    ["Algorithm",             "RandomForestRegressor"],
                ]
                t4 = Table(waste_data_pdf, colWidths=[7*cm, 8*cm])
                t4.setStyle(TableStyle([
                    ('BACKGROUND',  (0,0), (-1,0), BLUE),
                    ('TEXTCOLOR',   (0,0), (-1,0), colors.white),
                    ('FONTNAME',    (0,0), (-1,0), 'Helvetica-Bold'),
                    ('FONTSIZE',    (0,0), (-1,-1), 10),
                    ('ROWBACKGROUNDS',(0,1),(-1,-1),[CARD, colors.HexColor('#111b2e')]),
                    ('TEXTCOLOR',   (0,1), (-1,-1), LIGHT),
                    ('GRID',        (0,0), (-1,-1), 0.5, colors.HexColor('#1e2d45')),
                    ('PADDING',     (0,0), (-1,-1), 8),
                ]))
                story.append(t4)
                story.append(Spacer(1, 8))

            if include_rec:
                story.append(Paragraph("RECOMMENDATIONS", heading_style))
                if fr_rep >= 65:
                    recs = ["Issue immediate public flood warning", "Close all low-lying roads and underpasses",
                            "Deploy emergency drainage pumps", "Alert NDMA and provincial disaster management",
                            "Begin evacuation of flood-prone neighborhoods", "Open emergency relief camps"]
                elif fr_rep >= 40:
                    recs = ["Monitor rainfall every 2 hours", "Inspect drainage systems and nullahs",
                            "Put emergency response teams on standby", "Issue advisory to residents in low-lying areas",
                            "Coordinate with PDMA for resource pre-positioning"]
                else:
                    recs = ["Continue routine environmental monitoring", "Maintain drainage and flood infrastructure",
                            "Update risk assessments before monsoon season", "Conduct community awareness programs"]
                for rec in recs:
                    story.append(Paragraph(f"• {rec}", body_style))

            # Footer
            story.append(Spacer(1, 16))
            story.append(HRFlowable(width="100%", thickness=0.5, color=GREY))
            story.append(Paragraph(
                f"AI-Driven Urban Management System | GCUF BSDS Final Year Project 2026 | {datetime.now().strftime('%d %b %Y')}",
                ParagraphStyle('footer', fontSize=8, textColor=GREY, alignment=TA_CENTER, spaceBefore=8)))

            doc.build(story)
            pdf_bytes = buffer.getvalue()
            buffer.close()

            st.success("✅ PDF generated successfully!")
            st.download_button(
                label="📥 Download PDF Report",
                data=pdf_bytes,
                file_name=f"{report_city}_risk_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                mime="application/pdf"
            )

        except ImportError:
            st.error("Run: pip install reportlab")
        except Exception as e:
            st.error(f"Error generating PDF: {str(e)}")

