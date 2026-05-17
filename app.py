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
try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY = True
except ImportError:
    PLOTLY = False
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
# PAKISTAN CITY SEARCH (All 200+ cities via geocoding)
# ═══════════════════════════════════════════════════════════════
@st.cache_data(ttl=86400)
def search_pakistan_city(city_name):
    """Search any Pakistani city using Open-Meteo geocoding API"""
    try:
        r = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city_name, "count": 10, "language": "en", "format": "json"},
            timeout=8
        )
        if r.status_code == 200:
            results = r.json().get("results", [])
            # Filter for Pakistan only
            pak = [x for x in results if x.get("country_code") == "PK"]
            if pak:
                best = pak[0]
                return {
                    "name":     best.get("name", city_name),
                    "lat":      best.get("latitude"),
                    "lon":      best.get("longitude"),
                    "province": best.get("admin1", "Pakistan"),
                    "pop":      best.get("population", 0),
                    "coastal":  False,
                    "reason":   f"Located in {best.get('admin1','Pakistan')}, Pakistan",
                    "found":    True
                }
    except Exception:
        pass
    return {"found": False}

@st.cache_data(ttl=600)
def get_weather_by_coords(lat, lon):
    """Get weather for any coordinates"""
    url = (f"https://api.open-meteo.com/v1/forecast?"
           f"latitude={lat}&longitude={lon}"
           f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,"
           f"precipitation,rain,wind_speed_10m,weather_code"
           f"&hourly=precipitation_probability"
           f"&forecast_days=1&timezone=Asia%2FKarachi")
    try:
        r = requests.get(url, timeout=8)
        if r.status_code == 200:
            d = r.json(); cu = d["current"]
            return {
                "temp":     round(cu["temperature_2m"],1),
                "feels":    round(cu["apparent_temperature"],1),
                "hum":      cu["relative_humidity_2m"],
                "precip":   cu["precipitation"],
                "rain":     cu["rain"],
                "wind":     cu["wind_speed_10m"],
                "rp":       max(d["hourly"]["precipitation_probability"][:6]),
                "code":     cu["weather_code"],
                "fc":       None,
                "live":     True
            }
    except Exception:
        pass
    return {"temp":35,"feels":38,"hum":60,"precip":0,"rain":0,
            "wind":12,"rp":10,"code":0,"fc":None,"live":False}

def flood_risk_custom(city_info, weather):
    """Compute flood risk for any custom city"""
    season = get_season()
    # Use default profile (moderate risk)
    s = dict(infrastructure=6,urbanization=6,drainage=6,dams=5,
             deforestation=5,encroachments=5,agriculture=5,
             planning=6,political=5,preparedness=5,topography=5,
             river=6,coastal=0,landslide=3,watersheds=5,
             siltation=5,population=6,wetland_loss=5,climate_change=5)
    mn = min(10,(weather["precip"]/5)+(weather["rp"]/15))
    raw = {
        "MonsoonIntensity":mn,"TopographyDrainage":s["topography"],
        "RiverManagement":s["river"],"Deforestation":s["deforestation"],
        "Urbanization":s["urbanization"],"ClimateChange":s["climate_change"],
        "DamsQuality":s["dams"],"Siltation":s["siltation"],
        "AgriculturalPractices":s["agriculture"],"Encroachments":s["encroachments"],
        "IneffectiveDisasterPreparedness":s["preparedness"],
        "DrainageSystems":s["drainage"],"CoastalVulnerability":s["coastal"],
        "Landslides":s["landslide"],"Watersheds":s["watersheds"],
        "DeterioratingInfrastructure":s["infrastructure"],
        "PopulationScore":s["population"],"WetlandLoss":s["wetland_loss"],
        "InadequatePlanning":s["planning"],"PoliticalFactors":s["political"],
    }
    raw["Infrastructure_Risk"]=(raw["DeterioratingInfrastructure"]+raw["DrainageSystems"]+raw["DamsQuality"])/3
    raw["Human_Activity_Risk"]=(raw["Deforestation"]+raw["Urbanization"]+raw["AgriculturalPractices"]+raw["Encroachments"])/4
    raw["Climate_Risk"]=(raw["MonsoonIntensity"]+raw["ClimateChange"]+raw["WetlandLoss"])/3
    raw["Governance_Risk"]=(raw["IneffectiveDisasterPreparedness"]+raw["InadequatePlanning"]+raw["PoliticalFactors"])/3
    raw["Total_Risk_Score"]=raw["Infrastructure_Risk"]+raw["Human_Activity_Risk"]+raw["Climate_Risk"]+raw["Governance_Risk"]
    return float(np.clip(FM.predict(pd.DataFrame([raw])[FF])[0]*season["fm"],0,1))

# ── Plotly chart helpers ───────────────────────────────────────
def plotly_gauge(value, title, color):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text":title,"font":{"color":"#e8edf5","size":14}},
        number={"suffix":"%","font":{"color":color,"size":36}},
        gauge={
            "axis":{"range":[0,100],"tickcolor":"#3d5170","tickfont":{"color":"#7a8ea8"}},
            "bar":{"color":color,"thickness":0.3},
            "bgcolor":"#0d1421",
            "bordercolor":"#1e2d45",
            "steps":[
                {"range":[0,40],"color":"#071a12"},
                {"range":[40,65],"color":"#2d2515"},
                {"range":[65,100],"color":"#2d0f0f"},
            ],
            "threshold":{"line":{"color":color,"width":3},"value":value}
        }
    ))
    fig.update_layout(
        paper_bgcolor="#080c14", plot_bgcolor="#080c14",
        font={"color":"#e8edf5"}, height=220,
        margin=dict(l=20,r=20,t=40,b=20)
    )
    return fig

def plotly_bar(cities, values, title, color_fn):
    colors = [color_fn(v) for v in values]
    fig = go.Figure(go.Bar(
        x=values, y=cities, orientation="h",
        marker_color=colors,
        text=[f"{v:.0f}%" for v in values],
        textposition="outside",
        textfont={"color":"#e8edf5","size":11}
    ))
    fig.update_layout(
        title={"text":title,"font":{"color":"#e8edf5","size":13}},
        paper_bgcolor="#080c14", plot_bgcolor="#0d1421",
        font={"color":"#7a8ea8"},
        xaxis={"range":[0,110],"gridcolor":"#1e2d45","color":"#7a8ea8"},
        yaxis={"gridcolor":"#1e2d45","color":"#e8edf5"},
        height=380, margin=dict(l=120,r=60,t=40,b=20)
    )
    return fig

def plotly_line(x, y, title, color="#3b82f6", y2=None, y2_name=None):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y, mode="lines+markers",
        line=dict(color=color,width=2.5),
        marker=dict(size=6,color=color),
        fill="tozeroy", fillcolor=f"rgba(59,130,246,0.1)"
    ))
    if y2 is not None:
        fig.add_trace(go.Scatter(
            x=x, y=y2, mode="lines",
            name=y2_name, line=dict(color="#f59e0b",width=1.5,dash="dash"),
            yaxis="y2"
        ))
    fig.update_layout(
        title={"text":title,"font":{"color":"#e8edf5","size":13}},
        paper_bgcolor="#080c14", plot_bgcolor="#0d1421",
        font={"color":"#7a8ea8"},
        xaxis={"gridcolor":"#1e2d45","color":"#7a8ea8"},
        yaxis={"gridcolor":"#1e2d45","color":"#7a8ea8"},
        height=320, margin=dict(l=40,r=40,t=40,b=40),
        showlegend=False
    )
    return fig


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
# CITY SEARCH ENGINE
# ═══════════════════════════════════════════════════════════════
@st.cache_data(ttl=3600)
def search_city_pakistan(query):
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={query}&count=10&language=en&format=json"
        r = requests.get(url, timeout=8)
        if r.status_code == 200:
            results = r.json().get("results", [])
            return [x for x in results if x.get("country_code") == "PK"]
    except: pass
    return []

@st.cache_data(ttl=600)
def get_weather_coords(lat, lon):
    url = (f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
           f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,"
           f"precipitation,rain,wind_speed_10m,weather_code"
           f"&hourly=precipitation_probability"
           f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,"
           f"precipitation_probability_max,weathercode"
           f"&forecast_days=7&timezone=Asia%2FKarachi")
    try:
        r = requests.get(url, timeout=8)
        if r.status_code == 200:
            d = r.json(); cu = d["current"]
            return {"temp":round(cu["temperature_2m"],1),
                    "feels":round(cu["apparent_temperature"],1),
                    "hum":cu["relative_humidity_2m"],"precip":cu["precipitation"],
                    "rain":cu["rain"],"wind":cu["wind_speed_10m"],
                    "rp":max(d["hourly"]["precipitation_probability"][:6]),
                    "code":cu["weather_code"],"fc":d["daily"],"live":True}
    except: pass
    return {"temp":35,"feels":38,"hum":60,"precip":0,"rain":0,
            "wind":12,"rp":10,"code":0,"fc":None,"live":False}

def flood_risk_any(lat, lon, pop=6, coastal=False, w=None):
    if w is None: w = get_weather_coords(lat, lon)
    season = get_season()
    mn = min(10, (w["precip"]/5) + (w["rp"]/15))
    raw = {
        "MonsoonIntensity":mn,"TopographyDrainage":5,"RiverManagement":5,
        "Deforestation":5,"Urbanization":min(10,pop),"ClimateChange":5,
        "DamsQuality":5,"Siltation":5,"AgriculturalPractices":5,
        "Encroachments":5,"IneffectiveDisasterPreparedness":5,
        "DrainageSystems":5,"CoastalVulnerability":8 if coastal else 3,
        "Landslides":3,"Watersheds":5,"DeterioratingInfrastructure":5,
        "PopulationScore":pop,"WetlandLoss":5,"InadequatePlanning":5,"PoliticalFactors":5,
    }
    raw["Infrastructure_Risk"]=(raw["DeterioratingInfrastructure"]+raw["DrainageSystems"]+raw["DamsQuality"])/3
    raw["Human_Activity_Risk"]=(raw["Deforestation"]+raw["Urbanization"]+raw["AgriculturalPractices"]+raw["Encroachments"])/4
    raw["Climate_Risk"]=(raw["MonsoonIntensity"]+raw["ClimateChange"]+raw["WetlandLoss"])/3
    raw["Governance_Risk"]=(raw["IneffectiveDisasterPreparedness"]+raw["InadequatePlanning"]+raw["PoliticalFactors"])/3
    raw["Total_Risk_Score"]=raw["Infrastructure_Risk"]+raw["Human_Activity_Risk"]+raw["Climate_Risk"]+raw["Governance_Risk"]
    base = float(np.clip(FM.predict(pd.DataFrame([raw])[FF])[0], 0, 1))
    return float(np.clip(base * season["fm"], 0, 1)), w

def heat_risk_any(w):
    season = get_season()
    t,fl,h = w["temp"],w["feels"],w["hum"]
    sc = 0
    if t>=48: sc+=40
    elif t>=45: sc+=30
    elif t>=42: sc+=20
    elif t>=38: sc+=10
    elif t>=35: sc+=5
    if fl>t+3: sc+=8
    if h>60 and t>35: sc+=10
    return min(100, round(sc*season["hm"], 1))

@st.cache_data(ttl=900)
def get_top10_flood():
    results = []
    for cn, ci in CITIES.items():
        try:
            w  = get_weather(cn)
            fr = flood_risk(cn, w)*100
            results.append({"city":cn,"province":ci["province"],
                            "flood":fr,"temp":w["temp"],"rp":w["rp"],
                            "reason":ci["reason"][:60]})
        except: pass
    return sorted(results, key=lambda x:x["flood"], reverse=True)[:10]

@st.cache_data(ttl=900)
def get_top10_heat():
    results = []
    for cn, ci in CITIES.items():
        try:
            w  = get_weather(cn)
            hr = heat_risk(w, cn)
            results.append({"city":cn,"province":ci["province"],
                            "heat":hr,"temp":w["temp"],"feels":w["feels"]})
        except: pass
    return sorted(results, key=lambda x:x["heat"], reverse=True)[:10]

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
# ── Firebase Auth Config ─────────────────────────────────────
FIREBASE_API_KEY = "AIzaSyCB1xbTHFRKOY4m9JQbqySRNkaT1w-FPv4"
FIREBASE_SIGN_IN = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
FIREBASE_SIGN_UP = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_API_KEY}"

def firebase_login(email, password):
    try:
        r = httpx.post(FIREBASE_SIGN_IN,
            json={"email":email,"password":password,"returnSecureToken":True},timeout=10)
        d = r.json()
        if "idToken" in d:
            return {"name":d.get("displayName",email.split("@")[0]),
                    "email":d["email"],
                    "picture":f"https://ui-avatars.com/api/?name={d.get('displayName',email.split('@')[0]).replace(' ','+')}&background=3b82f6&color=fff&size=128&bold=true",
                    "token":d["idToken"]}, None
        msg = d.get("error",{}).get("message","Login failed")
        msg = msg.replace("EMAIL_NOT_FOUND","Email not registered")                 .replace("INVALID_PASSWORD","Wrong password")                 .replace("INVALID_LOGIN_CREDENTIALS","Invalid email or password")                 .replace("TOO_MANY_ATTEMPTS_TRY_LATER","Too many attempts, try later")
        return None, msg
    except Exception as e: return None, str(e)

def firebase_signup(email, password, name):
    try:
        r = httpx.post(FIREBASE_SIGN_UP,
            json={"email":email,"password":password,"returnSecureToken":True},timeout=10)
        d = r.json()
        if "idToken" in d:
            display = name or email.split("@")[0]
            return {"name":display,"email":d["email"],
                    "picture":f"https://ui-avatars.com/api/?name={display.replace(' ','+')}&background=3b82f6&color=fff&size=128&bold=true",
                    "token":d["idToken"]}, None
        msg = d.get("error",{}).get("message","Signup failed")
        msg = msg.replace("EMAIL_EXISTS","Email already registered, try signing in")                 .replace("WEAK_PASSWORD","Password must be at least 6 characters")
        return None, msg
    except Exception as e: return None, str(e)

def google_auto_login(gmail):
    """Auto login/signup with Gmail — looks like Google OAuth"""
    try:
        # Try login first
        auto_pass = "GoogleAuth_" + gmail.split("@")[0] + "_2026"
        r = httpx.post(FIREBASE_SIGN_IN,
            json={"email":gmail,"password":auto_pass,"returnSecureToken":True},timeout=10)
        d = r.json()
        if "idToken" in d:
            name = gmail.split("@")[0].replace("."," ").title()
            pic  = f"https://ui-avatars.com/api/?name={name.replace(' ','+')}&background=EA4335&color=fff&size=128&bold=true"
            return {"name":name,"email":gmail,"picture":pic,"token":d["idToken"],"google":True}, None
        # If not found, auto-register
        r2 = httpx.post(FIREBASE_SIGN_UP,
            json={"email":gmail,"password":auto_pass,"returnSecureToken":True},timeout=10)
        d2 = r2.json()
        if "idToken" in d2:
            name = gmail.split("@")[0].replace("."," ").title()
            pic  = f"https://ui-avatars.com/api/?name={name.replace(' ','+')}&background=EA4335&color=fff&size=128&bold=true"
            return {"name":name,"email":gmail,"picture":pic,"token":d2["idToken"],"google":True}, None
        return None, "Could not sign in with Google"
    except Exception as e: return None, str(e)

# ── Session ───────────────────────────────────────────────────
for k,v in [("auth_user",None),("auth_tab","login"),("auth_err",""),("show_google",False)]:
    if k not in st.session_state: st.session_state[k]=v

# ── Login Page ────────────────────────────────────────────────
if not st.session_state.auth_user:
    st.markdown("""
    <style>
    .stApp{background:radial-gradient(ellipse at 20% 50%,#0a1628 0%,#060910 60%,#080c14 100%)!important}
    #MainMenu,footer,header{visibility:hidden}
    .stTabs [data-baseweb="tab-list"]{background:transparent!important;border-bottom:1px solid #1e2d45!important;gap:0!important}
    .stTabs [data-baseweb="tab"]{color:#7a8ea8!important;font-size:.88rem!important;padding:10px 24px!important;background:transparent!important;border-radius:0!important}
    .stTabs [aria-selected="true"]{color:#e8edf5!important;border-bottom:2px solid #3b82f6!important;background:transparent!important}
    .stTextInput>div>div>input{background:#0d1829!important;border:1px solid #1e2d45!important;color:#e8edf5!important;border-radius:10px!important;padding:14px 16px!important;font-size:.9rem!important}
    .stTextInput>div>div>input:focus{border-color:#3b82f6!important;box-shadow:0 0 0 3px rgba(59,130,246,.2)!important}
    .stTextInput label{color:#7a8ea8!important;font-size:.82rem!important;margin-bottom:4px!important}
    .stButton>button{border-radius:12px!important;padding:14px 20px!important;font-weight:600!important;font-size:.92rem!important;width:100%!important;transition:all .2s!important}
    .stButton>button[kind="primary"]{background:linear-gradient(135deg,#3b82f6 0%,#1d4ed8 100%)!important;border:none!important;color:white!important;box-shadow:0 4px 15px rgba(59,130,246,.3)!important}
    .stButton>button[kind="secondary"]{background:#0d1829!important;border:1px solid #1e2d45!important;color:#e8edf5!important}
    div[data-testid="stVerticalBlock"]{gap:.5rem!important}
    </style>""", unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 1.2, 1])
    with mid:
        st.markdown("""
        <div style="text-align:center;padding:36px 0 24px">
          <div style="width:72px;height:72px;background:linear-gradient(135deg,#1d4ed8,#3b82f6);
                      border-radius:20px;display:inline-flex;align-items:center;justify-content:center;
                      font-size:2rem;margin-bottom:16px;box-shadow:0 8px 32px rgba(59,130,246,.3)">🏙️</div>
          <div style="font-family:'Space Mono',monospace;font-size:1.7rem;font-weight:700;
                      color:#e8edf5;letter-spacing:-.02em">Urban AI System</div>
          <div style="color:#3b82f6;font-size:.75rem;margin-top:8px;letter-spacing:.12em;text-transform:uppercase">
            Pakistan · GCUF BSDS 2026</div>
          <div style="color:#3d5170;font-size:.76rem;margin-top:4px">AI-Driven Urban Management</div>
        </div>""", unsafe_allow_html=True)

        st.markdown("""<div style="background:rgba(10,15,25,.95);border:1px solid #1a2a3f;
                    border-radius:24px;padding:32px 28px 24px;
                    box-shadow:0 32px 64px rgba(0,0,0,.6)">""", unsafe_allow_html=True)

        # ── Google Login Panel ────────────────────────────────
        if st.session_state.show_google:
            st.markdown("""
            <div style="text-align:center;margin-bottom:16px">
              <div style="font-size:1.8rem;margin-bottom:8px">
                <svg width="32" height="32" viewBox="0 0 48 48" style="vertical-align:middle">
                  <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>
                  <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>
                  <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>
                  <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/>
                </svg>
              </div>
              <div style="color:#e8edf5;font-size:1rem;font-weight:600">Sign in with Google</div>
              <div style="color:#7a8ea8;font-size:.78rem;margin-top:4px">Enter your Gmail address to continue</div>
            </div>""", unsafe_allow_html=True)

            if st.session_state.auth_err:
                st.markdown(f'<div style="background:#1a0808;border:1px solid #dc2626;color:#fca5a5;border-radius:10px;padding:10px 14px;font-size:.82rem;margin-bottom:8px">⚠️ {st.session_state.auth_err}</div>', unsafe_allow_html=True)

            gmail_input = st.text_input("Gmail address", placeholder="yourname@gmail.com", key="gmail_in")

            c1, c2 = st.columns(2)
            with c1:
                if st.button("← Back", use_container_width=True):
                    st.session_state.show_google = False
                    st.session_state.auth_err    = ""
                    st.rerun()
            with c2:
                if st.button("Continue →", type="primary", use_container_width=True):
                    if not gmail_input or "@" not in gmail_input:
                        st.session_state.auth_err = "Please enter a valid Gmail address"
                        st.rerun()
                    elif "gmail.com" not in gmail_input.lower():
                        st.session_state.auth_err = "Please use a Gmail address (@gmail.com)"
                        st.rerun()
                    else:
                        with st.spinner("Signing in with Google..."):
                            user, err = google_auto_login(gmail_input.lower().strip())
                        if user:
                            st.session_state.auth_user  = user
                            st.session_state.auth_err   = ""
                            st.session_state.show_google= False
                            st.rerun()
                        else:
                            st.session_state.auth_err = err
                            st.rerun()

        else:
            # ── Main Login/Signup Tabs ────────────────────────
            tab_l, tab_s = st.tabs(["🔑  Sign In", "✨  Create Account"])

            with tab_l:
                st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

                if st.session_state.auth_err and st.session_state.auth_tab=="login":
                    st.markdown(f'<div style="background:#1a0808;border:1px solid #dc2626;color:#fca5a5;border-radius:10px;padding:10px 14px;font-size:.82rem;margin-bottom:8px">⚠️ {st.session_state.auth_err}</div>', unsafe_allow_html=True)

                email_l = st.text_input("Email address", placeholder="you@example.com", key="le")
                pass_l  = st.text_input("Password", type="password", placeholder="Enter your password", key="lp")
                st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

                if st.button("Sign In →", type="primary", use_container_width=True, key="btn_l"):
                    if not email_l or not pass_l:
                        st.session_state.auth_err="Please enter email and password"
                        st.session_state.auth_tab="login"; st.rerun()
                    user,err = firebase_login(email_l, pass_l)
                    if user:
                        st.session_state.auth_user=user; st.session_state.auth_err=""; st.rerun()
                    else:
                        st.session_state.auth_err=err; st.session_state.auth_tab="login"; st.rerun()

                st.markdown("""<div style="display:flex;align-items:center;gap:12px;margin:18px 0 14px;color:#3d5170;font-size:.75rem">
                  <div style="flex:1;height:1px;background:linear-gradient(90deg,transparent,#1e2d45)"></div>or<div style="flex:1;height:1px;background:linear-gradient(90deg,#1e2d45,transparent)"></div>
                </div>""", unsafe_allow_html=True)

                # Google button
                if st.button("🔴  Continue with Google", use_container_width=True, key="g_login"):
                    st.session_state.show_google = True
                    st.session_state.auth_err    = ""
                    st.rerun()

            with tab_s:
                st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

                if st.session_state.auth_err and st.session_state.auth_tab=="signup":
                    st.markdown(f'<div style="background:#1a0808;border:1px solid #dc2626;color:#fca5a5;border-radius:10px;padding:10px 14px;font-size:.82rem;margin-bottom:8px">⚠️ {st.session_state.auth_err}</div>', unsafe_allow_html=True)

                name_s  = st.text_input("Full Name", placeholder="Ahmad Raza", key="sn")
                email_s = st.text_input("Email address", placeholder="you@example.com", key="se")
                pass_s  = st.text_input("Password", type="password", placeholder="Min. 6 characters", key="sp")
                pass_c  = st.text_input("Confirm Password", type="password", placeholder="Repeat password", key="sc")
                st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

                if st.button("Create Account →", type="primary", use_container_width=True, key="btn_s"):
                    if not all([name_s,email_s,pass_s,pass_c]):
                        st.session_state.auth_err="Please fill in all fields"
                        st.session_state.auth_tab="signup"; st.rerun()
                    elif pass_s != pass_c:
                        st.session_state.auth_err="Passwords do not match"
                        st.session_state.auth_tab="signup"; st.rerun()
                    elif len(pass_s) < 6:
                        st.session_state.auth_err="Password must be at least 6 characters"
                        st.session_state.auth_tab="signup"; st.rerun()
                    else:
                        user,err = firebase_signup(email_s,pass_s,name_s)
                        if user:
                            st.session_state.auth_user=user; st.session_state.auth_err=""; st.rerun()
                        else:
                            st.session_state.auth_err=err; st.session_state.auth_tab="signup"; st.rerun()

                st.markdown("""<div style="display:flex;align-items:center;gap:12px;margin:18px 0 14px;color:#3d5170;font-size:.75rem">
                  <div style="flex:1;height:1px;background:linear-gradient(90deg,transparent,#1e2d45)"></div>or<div style="flex:1;height:1px;background:linear-gradient(90deg,#1e2d45,transparent)"></div>
                </div>""", unsafe_allow_html=True)

                if st.button("🔴  Sign up with Google", use_container_width=True, key="g_signup"):
                    st.session_state.show_google = True
                    st.session_state.auth_err    = ""
                    st.rerun()

        st.markdown("""</div>
        <div style="text-align:center;color:#2d3f55;font-size:.68rem;margin-top:12px;padding-bottom:20px">
          🔒 Secured by Firebase Authentication · Urban AI System · GCUF 2026
        </div>""", unsafe_allow_html=True)

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
        "🔍  City Search",
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
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.auth_user  = None
        st.session_state.auth_error = ""
        st.rerun()

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
if "City Search" in page:
    st.markdown("# 🔍 City Search")
    st.markdown("Search any city in Pakistan — live weather, flood risk & heatwave analysis")
    st.markdown("---")

    # Search box
    col_s, col_b = st.columns([4,1])
    with col_s:
        query = st.text_input("", placeholder="🔍  Type any Pakistani city... e.g. Sialkot, Gwadar, Mirpur",
                              label_visibility="collapsed", key="city_search_q")
    with col_b:
        search_btn = st.button("Search", type="primary", use_container_width=True)

    if query and (search_btn or len(query) > 2):
        with st.spinner(f"Searching for {query}..."):
            results = search_city_pakistan(query)

        if not results:
            st.markdown(f"""
            <div class="alert a-warn">
              ⚠️ No Pakistani city found for <b>"{query}"</b>.
              Try a different spelling or nearby city name.
            </div>""", unsafe_allow_html=True)
        else:
            # Show top result prominently
            top = results[0]
            lat, lon = top["latitude"], top["longitude"]
            city_name = top["name"]
            admin = top.get("admin1", "Pakistan")

            with st.spinner(f"Fetching live data for {city_name}..."):
                w  = get_weather_coords(lat, lon)
                fr, _ = flood_risk_any(lat, lon, w=w)
                hr = heat_risk_any(w)

            fr_pct = fr * 100
            hl, hc, he = hlabel(hr)
            fc = rcol(fr_pct)
            season = get_season()

            # City header
            st.markdown(f"""
            <div class="card" style="border-color:#3b82f6;margin-bottom:16px">
              <div style="display:flex;justify-content:space-between;align-items:start;flex-wrap:wrap;gap:8px">
                <div>
                  <div style="font-family:monospace;font-size:1.4rem;font-weight:700;color:#e8edf5">{city_name}</div>
                  <div style="color:#7a8ea8;font-size:.82rem">{admin} · Pakistan · {lat:.2f}°N {lon:.2f}°E</div>
                </div>
                <div style="text-align:right">
                  <span class="badge b-b">{'🟢 Live' if w['live'] else '🟡 Cached'}</span>
                </div>
              </div>
            </div>""", unsafe_allow_html=True)

            # Risk metrics
            c1,c2,c3,c4 = st.columns(4)
            with c1:
                st.markdown(f"""
                <div class="kpi" style="border-color:{fc}40">
                  <div class="kpi-v" style="color:{fc}">{fr_pct:.1f}%</div>
                  <div class="kpi-l">🌊 Flood Risk</div>
                </div>""", unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div class="kpi" style="border-color:{hc}40">
                  <div class="kpi-v" style="color:{hc}">{hr:.1f}%</div>
                  <div class="kpi-l">🌡️ Heat Risk</div>
                </div>""", unsafe_allow_html=True)
            with c3:
                st.markdown(f"""
                <div class="kpi">
                  <div class="kpi-v" style="color:#e8edf5">{w['temp']}°C</div>
                  <div class="kpi-l">🌡️ Temperature</div>
                </div>""", unsafe_allow_html=True)
            with c4:
                st.markdown(f"""
                <div class="kpi">
                  <div class="kpi-v" style="color:#3b82f6">{w['rp']}%</div>
                  <div class="kpi-l">🌧️ Rain Chance</div>
                </div>""", unsafe_allow_html=True)

            st.markdown("---")
            cl, cr = st.columns(2)

            with cl:
                st.markdown('<div class="sec">Current Weather</div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="card">
                  <div style="font-size:2rem;margin-bottom:8px">{wemoji(w['code'])}</div>
                  <div style="font-family:monospace;font-size:1.8rem;color:#e8edf5;font-weight:700">{w['temp']}°C</div>
                  <div style="color:#7a8ea8;font-size:.82rem;margin:4px 0">Feels like {w['feels']}°C</div>
                  <div style="display:flex;flex-wrap:wrap;gap:5px;margin-top:10px">
                    <span class="badge b-b">💧 {w['hum']}% humidity</span>
                    <span class="badge b-b">💨 {w['wind']} km/h wind</span>
                    <span class="badge b-b">🌧️ {w['rp']}% rain</span>
                    <span class="badge b-b">🌡️ {w['precip']}mm precip</span>
                  </div>
                </div>""", unsafe_allow_html=True)

                # Flood alert
                if fr_pct >= 65:
                    st.markdown(f'<div class="alert a-crit"><b>⚠️ HIGH FLOOD RISK — {city_name}</b><br>🚨 Issue warnings · 🚧 Close low roads · 📢 Alert NDMA</div>', unsafe_allow_html=True)
                elif fr_pct >= 40:
                    st.markdown(f'<div class="alert a-warn"><b>⚡ MEDIUM FLOOD RISK — {city_name}</b><br>📡 Monitor closely · 🔍 Check drainage</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="alert a-ok"><b>✅ LOW FLOOD RISK — {city_name}</b><br>📊 Normal conditions</div>', unsafe_allow_html=True)

            with cr:
                st.markdown('<div class="sec">Risk Assessment</div>', unsafe_allow_html=True)

                # Flood gauge
                st.markdown(f"""
                <div class="card">
                  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
                    <span style="color:#7a8ea8;font-size:.82rem">🌊 Flood Probability</span>
                    <span style="font-family:monospace;font-weight:700;color:{fc}">{fr_pct:.1f}%</span>
                  </div>
                  <div style="background:#1e2d45;border-radius:6px;height:10px;overflow:hidden;margin-bottom:16px">
                    <div style="width:{fr_pct}%;height:100%;background:linear-gradient(90deg,{fc}88,{fc});border-radius:6px;transition:width .5s"></div>
                  </div>
                  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
                    <span style="color:#7a8ea8;font-size:.82rem">🌡️ Heatwave Risk</span>
                    <span style="font-family:monospace;font-weight:700;color:{hc}">{hr:.1f}%</span>
                  </div>
                  <div style="background:#1e2d45;border-radius:6px;height:10px;overflow:hidden">
                    <div style="width:{hr}%;height:100%;background:linear-gradient(90deg,{hc}88,{hc});border-radius:6px;transition:width .5s"></div>
                  </div>
                  <div style="margin-top:14px;font-size:.75rem;color:#3d5170">
                    {season['e']} Season: {season['name']} · Risk adjusted for current conditions
                  </div>
                </div>""", unsafe_allow_html=True)

                # Heat alert
                if hr >= 70:
                    st.markdown(f'<div class="alert a-crit"><b>🌡️ EXTREME HEAT — {city_name}</b><br>⚕️ Open cooling centers · 🚰 Distribute water</div>', unsafe_allow_html=True)
                elif hr >= 50:
                    st.markdown(f'<div class="alert a-warn"><b>⚠️ HIGH HEAT RISK — {city_name}</b><br>💧 Stay hydrated · 🌳 Avoid direct sun</div>', unsafe_allow_html=True)

            # Other results
            if len(results) > 1:
                st.markdown("---")
                st.markdown('<div class="sec">Other Matching Cities</div>', unsafe_allow_html=True)
                other_cols = st.columns(min(4, len(results)-1))
                for i, res in enumerate(results[1:5]):
                    with other_cols[i % 4]:
                        st.markdown(f"""
                        <div class="card" style="text-align:center;cursor:pointer">
                          <div style="color:#e8edf5;font-weight:600;font-size:.88rem">{res['name']}</div>
                          <div style="color:#7a8ea8;font-size:.72rem">{res.get('admin1','Pakistan')}</div>
                          <div style="color:#3d5170;font-size:.68rem;margin-top:4px">{res['latitude']:.2f}°N {res['longitude']:.2f}°E</div>
                        </div>""", unsafe_allow_html=True)
    else:
        # Show top 10 rankings when no search
        st.markdown('<div class="sec">🏆 Top 10 Highest Flood Risk Cities — Right Now</div>', unsafe_allow_html=True)
        with st.spinner("Loading top flood risk cities..."):
            top_flood = get_top10_flood()

        for i, d in enumerate(top_flood):
            fc2 = rcol(d['flood'])
            medal = "🥇" if i==0 else "🥈" if i==1 else "🥉" if i==2 else f"{i+1}."
            st.markdown(f"""
            <div class="alert {'a-crit' if d['flood']>=65 else 'a-warn' if d['flood']>=40 else 'a-ok'}" style="margin:4px 0">
              <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px">
                <div>
                  <span style="font-size:.9rem">{medal}</span>
                  <b style="margin-left:6px">{d['city']}</b>
                  <span class="badge b-b" style="margin-left:6px">{d['province']}</span>
                </div>
                <div style="display:flex;align-items:center;gap:12px">
                  <span style="color:#7a8ea8;font-size:.78rem">🌡️ {d['temp']}°C · 🌧️ {d['rp']}%</span>
                  <b style="font-family:monospace;color:{fc2};font-size:1rem">{d['flood']:.1f}%</b>
                </div>
              </div>
              <div style="font-size:.72rem;color:#7a8ea8;margin-top:4px">📍 {d['reason']}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<div class="sec">🌡️ Top 10 Highest Heatwave Risk Cities — Right Now</div>', unsafe_allow_html=True)
        with st.spinner("Loading top heatwave cities..."):
            top_heat = get_top10_heat()

        for i, d in enumerate(top_heat):
            hc2 = rcol(d['heat'])
            medal = "🥇" if i==0 else "🥈" if i==1 else "🥉" if i==2 else f"{i+1}."
            st.markdown(f"""
            <div class="alert {'a-crit' if d['heat']>=70 else 'a-warn' if d['heat']>=50 else 'a-ok'}" style="margin:4px 0">
              <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px">
                <div>
                  <span style="font-size:.9rem">{medal}</span>
                  <b style="margin-left:6px">{d['city']}</b>
                  <span class="badge b-b" style="margin-left:6px">{d['province']}</span>
                </div>
                <div style="display:flex;align-items:center;gap:12px">
                  <span style="color:#7a8ea8;font-size:.78rem">feels {d['feels']}°C</span>
                  <b style="font-family:monospace;color:{hc2};font-size:1rem">{d['temp']}°C · {d['heat']:.0f}%</b>
                </div>
              </div>
            </div>""", unsafe_allow_html=True)

elif "Overview" in page:
    st.markdown("# 🏙️ AI-Driven Urban Management System")
    st.markdown(f"##### Pakistan · {len(CITIES)} monitored cities · {season['e']} {season['name']} · Live weather")
    if season['w']:
        st.markdown(f'<div class="alert a-warn">⚠️ {season["w"]}</div>',unsafe_allow_html=True)

    # KPIs
    latest=WDF.sort_values('timestamp').groupby('bin_id').last().reset_index()
    crit=int((latest["fill_level_%"]>=85).sum())
    high=int(((latest["fill_level_%"]>=70)&(latest["fill_level_%"]<85)).sum())
    st.markdown(f"""
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:12px 0">
      <div class="kpi"><div class="kpi-v" style="color:#3b82f6">{len(CITIES)}</div><div class="kpi-l">Cities Monitored</div></div>
      <div class="kpi"><div class="kpi-v" style="color:#ef4444">{crit}</div><div class="kpi-l">Critical Bins</div></div>
      <div class="kpi"><div class="kpi-v" style="color:#f59e0b">{high}</div><div class="kpi-l">High Fill Bins</div></div>
      <div class="kpi"><div class="kpi-v" style="color:#10b981">0.992</div><div class="kpi-l">Flood Model R²</div></div>
      <div class="kpi"><div class="kpi-v" style="color:#8b5cf6">0.9998</div><div class="kpi-l">Waste Model R²</div></div>
    </div>""", unsafe_allow_html=True)

    # ── City Search ───────────────────────────────────────────
    st.markdown('<div class="sec">🔍 Search Any City in Pakistan</div>', unsafe_allow_html=True)
    search_col, btn_col = st.columns([4, 1])
    with search_col:
        search_q = st.text_input("", placeholder="Type any Pakistani city... e.g. Bahawalpur, Abbottabad, Mirpur", label_visibility="collapsed", key="overview_search")
    with btn_col:
        search_btn = st.button("Search 🔍", type="primary", use_container_width=True)

    if search_btn and search_q:
        with st.spinner(f"Searching {search_q}..."):
            city_data = search_pakistan_city(search_q)
        if city_data["found"]:
            w = get_weather_by_coords(city_data["lat"], city_data["lon"])
            fr = flood_risk_custom(city_data, w) * 100
            hr = heat_risk(w, "Karachi")  # use default profile
            hl, hc, he = hlabel(hr); frc = rcol(fr)
            st.markdown(f"""
            <div class="card" style="border-color:#3b82f6;margin-bottom:8px">
              <div style="display:flex;justify-content:space-between;align-items:start;flex-wrap:wrap;gap:8px">
                <div>
                  <b style="color:#3b82f6;font-size:1.1rem">{city_data['name']}</b>
                  <span style="color:#7a8ea8;font-size:.8rem"> · {city_data['province']}</span><br>
                  <span style="font-size:.75rem;color:#3d5170">{city_data['reason']}</span>
                </div>
                <div style="text-align:right">
                  <span style="font-size:1.4rem">{wemoji(w['code'])}</span>
                  <b style="font-family:monospace;font-size:1.3rem;color:#e8edf5"> {w['temp']}°C</b>
                </div>
              </div>
              <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:10px">
                <span class="badge b-b">💧 {w['hum']}%</span>
                <span class="badge b-b">🌧️ {w['rp']}% rain</span>
                <span class="badge b-b">💨 {w['wind']} km/h</span>
                <span class="badge {'b-r' if fr>=65 else 'b-a' if fr>=40 else 'b-g'}">🌊 Flood {fr:.1f}%</span>
                <span class="badge {'b-r' if hr>=70 else 'b-a' if hr>=50 else 'b-g'}">🌡️ Heat {hr:.1f}%</span>
              </div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="alert a-warn">⚠️ "{search_q}" not found in Pakistan. Try a different spelling.</div>', unsafe_allow_html=True)

    # ── Top 10 Rankings ───────────────────────────────────────
    st.markdown('<div class="sec">⚡ Top 10 Highest Risk Cities — Live</div>', unsafe_allow_html=True)

    with st.spinner("Computing live risk for all cities..."):
        city_risks = []
        for cn, ci in CITIES.items():
            w = get_weather(cn)
            fr = flood_risk(cn, w) * 100
            hr = heat_risk(w, cn)
            city_risks.append({"city":cn,"province":ci["province"],"flood":fr,"heat":hr,
                               "temp":w["temp"],"rp":w["rp"],"code":w["code"]})

    city_risks.sort(key=lambda x: x["flood"], reverse=True)
    top10_flood = city_risks[:10]
    top10_heat  = sorted(city_risks, key=lambda x: x["heat"], reverse=True)[:10]

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="sec">🌊 Top 10 Flood Risk</div>', unsafe_allow_html=True)
        for i, d in enumerate(top10_flood):
            col = rcol(d["flood"])
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;padding:8px 12px;
                        background:#0d1421;border-radius:8px;margin:4px 0;
                        border-left:3px solid {col}">
              <span style="font-family:monospace;color:#3d5170;font-size:.75rem;width:20px">#{i+1}</span>
              <span style="color:#e8edf5;font-size:.88rem;flex:1">{d['city']}</span>
              <span style="color:#7a8ea8;font-size:.75rem">{d['province']}</span>
              <span style="font-family:monospace;color:{col};font-weight:700">{d['flood']:.0f}%</span>
            </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="sec">🌡️ Top 10 Heatwave Risk</div>', unsafe_allow_html=True)
        for i, d in enumerate(top10_heat):
            _, hc, _ = hlabel(d["heat"])
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;padding:8px 12px;
                        background:#0d1421;border-radius:8px;margin:4px 0;
                        border-left:3px solid {hc}">
              <span style="font-family:monospace;color:#3d5170;font-size:.75rem;width:20px">#{i+1}</span>
              <span style="color:#e8edf5;font-size:.88rem;flex:1">{d['city']}</span>
              <span style="color:#7a8ea8;font-size:.75rem">{d['temp']}°C</span>
              <span style="font-family:monospace;color:{hc};font-weight:700">{d['heat']:.0f}%</span>
            </div>""", unsafe_allow_html=True)

    # ── Live City Cards ───────────────────────────────────────
    st.markdown('<div class="sec">📡 All Monitored Cities — Live Conditions</div>', unsafe_allow_html=True)
    city_cards_html = '<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:10px;margin:8px 0">'
    for d in city_risks:
        fb = 'b-r' if d['flood']>=65 else 'b-a' if d['flood']>=40 else 'b-g'
        _,hc2,_ = hlabel(d['heat'])
        hb = 'b-r' if d['heat']>=70 else 'b-a' if d['heat']>=50 else 'b-g'
        city_cards_html += f"""
        <div class="card" style="min-width:0">
          <div style="display:flex;justify-content:space-between;align-items:start">
            <b style="color:#e8edf5;font-size:.88rem">{d['city']}</b>
            <span style="font-size:.62rem;color:#3d5170">{d['province']}</span>
          </div>
          <div style="margin:5px 0">{wemoji(d['code'])}
            <b style="color:#e8edf5;font-family:monospace"> {d['temp']}°C</b>
          </div>
          <div style="display:flex;flex-wrap:wrap;gap:3px">
            <span class="badge b-b">💧{CITIES[d['city']].get('pop','N/A')}</span>
            <span class="badge b-b">🌧️{d['rp']}%</span>
          </div>
          <div style="display:flex;flex-wrap:wrap;gap:3px;margin-top:5px">
            <span class="badge {fb}">🌊{d['flood']:.0f}%</span>
            <span class="badge {hb}">🌡️{d['heat']:.0f}%</span>
          </div>
        </div>"""
    city_cards_html += '</div>'
    st.markdown(city_cards_html, unsafe_allow_html=True)


elif "Flood" in page:
    st.markdown("# 🌊 Flood Prediction Module")
    st.markdown("GradientBoosting · R²=0.9920 · MAE=0.0033 · Seasonal-adjusted · Live weather")
    if season["w"]:
        st.markdown(f'<div class="alert a-warn">{season["e"]} {season["w"]}</div>',unsafe_allow_html=True)
    st.markdown("---")

    # ── City Search ───────────────────────────────────────────
    st.markdown('<div class="sec">🔍 Search Any Pakistani City</div>', unsafe_allow_html=True)
    sc1, sc2 = st.columns([4,1])
    with sc1:
        flood_search = st.text_input("", placeholder="Search any city in Pakistan...", label_visibility="collapsed", key="flood_city_search")
    with sc2:
        flood_search_btn = st.button("Search 🔍", type="primary", use_container_width=True, key="flood_search_btn")

    if flood_search_btn and flood_search:
        with st.spinner(f"Fetching data for {flood_search}..."):
            found = search_pakistan_city(flood_search)
        if found["found"]:
            w_s = get_weather_by_coords(found["lat"], found["lon"])
            fr_s = flood_risk_custom(found, w_s) * 100
            hr_s = heat_risk(w_s, "Karachi")
            col_s = rcol(fr_s)
            st.markdown(f"""
            <div class="card" style="border-color:{col_s}">
              <div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px">
                <div>
                  <b style="color:{col_s};font-size:1.1rem">{found["name"]}</b>
                  <span style="color:#7a8ea8"> · {found["province"]}</span><br>
                  <span style="font-size:.78rem;color:#3d5170">{found["reason"]}</span>
                </div>
                <div style="text-align:right">
                  {wemoji(w_s["code"])} <b style="font-family:monospace;font-size:1.4rem;color:{col_s}">{fr_s:.1f}%</b><br>
                  <span style="font-size:.75rem;color:{col_s}">{"HIGH RISK" if fr_s>=65 else "MEDIUM RISK" if fr_s>=40 else "LOW RISK"}</span>
                </div>
              </div>
              <div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:8px">
                <span class="badge b-b">🌡️ {w_s["temp"]}°C</span>
                <span class="badge b-b">💧 {w_s["hum"]}%</span>
                <span class="badge b-b">🌧️ {w_s["rp"]}% rain</span>
                <span class="badge b-b">🌡️ Heat {hr_s:.0f}%</span>
              </div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="alert a-warn">⚠️ "{flood_search}" not found. Try different spelling.</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ── Top 10 Flood Risk Cities ──────────────────────────────
    st.markdown('<div class="sec">🏆 Top 10 Highest Flood Risk Cities — Right Now</div>', unsafe_allow_html=True)

    with st.spinner("Computing live flood risk..."):
        flood_rankings = []
        for cn, ci in CITIES.items():
            w = get_weather(cn)
            fr = flood_risk(cn, w) * 100
            flood_rankings.append({"city":cn,"province":ci["province"],"flood":fr,
                                   "temp":w["temp"],"rp":w["rp"],"hum":w["hum"],
                                   "precip":w["precip"],"code":w["code"]})
        flood_rankings.sort(key=lambda x: x["flood"], reverse=True)
        top10 = flood_rankings[:10]

    # Plotly bar chart
    if PLOTLY:
        fig = go.Figure(go.Bar(
            x=[d["flood"] for d in reversed(top10)],
            y=[d["city"] for d in reversed(top10)],
            orientation="h",
            marker_color=[rcol(d["flood"]) for d in reversed(top10)],
            text=[f"{d['flood']:.0f}%" for d in reversed(top10)],
            textposition="outside",
            textfont={"color":"#e8edf5","size":11}
        ))
        fig.add_vline(x=65, line_dash="dash", line_color="#ef4444", line_width=1,
                      annotation_text="High Risk", annotation_font_color="#ef4444")
        fig.add_vline(x=40, line_dash="dash", line_color="#f59e0b", line_width=1,
                      annotation_text="Medium", annotation_font_color="#f59e0b")
        fig.update_layout(
            title={"text":"Top 10 Flood Risk Cities — Live","font":{"color":"#e8edf5","size":14}},
            paper_bgcolor="#080c14", plot_bgcolor="#0d1421",
            font={"color":"#7a8ea8"},
            xaxis={"range":[0,115],"gridcolor":"#1e2d45","color":"#7a8ea8","title":"Flood Risk (%)"},
            yaxis={"gridcolor":"#1e2d45","color":"#e8edf5"},
            height=400, margin=dict(l=130,r=60,t=50,b=30)
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        for i,d in enumerate(top10):
            col = rcol(d["flood"])
            st.markdown(f'<div style="display:flex;align-items:center;gap:10px;padding:8px 12px;background:#0d1421;border-radius:8px;margin:3px 0;border-left:3px solid {col}"><span style="color:#3d5170;font-size:.75rem">#{i+1}</span><span style="color:#e8edf5;flex:1">{d["city"]}</span><span style="color:{col};font-family:monospace;font-weight:700">{d["flood"]:.0f}%</span></div>', unsafe_allow_html=True)

    # ── Detailed City Analysis ────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="sec">📊 Detailed City Analysis</div>', unsafe_allow_html=True)

    col_l, col_r = st.columns([1,1])
    with col_l:
        city = st.selectbox("Select City for Detailed Analysis", list(CITIES.keys()))
        with st.spinner(f"Loading {city}..."):
            w = get_weather(city)
        ci = CITIES[city]
        live_tag = "🟢 Live" if w["live"] else "🟡 Cached"
        st.markdown(f"""
        <div class="card">
          <div style="display:flex;justify-content:space-between">
            <b style="color:#3b82f6">📡 {city} — Current Weather</b>
            <span style="color:#10b981;font-size:.75rem">{live_tag}</span>
          </div>
          <div style="margin:10px 0">
            <span style="font-size:1.6rem">{wemoji(w["code"])}</span>
            <b style="font-family:monospace;font-size:1.5rem;color:#e8edf5"> {w["temp"]}°C</b>
            <span style="color:#3d5170"> feels {w["feels"]}°C</span>
          </div>
          <div style="display:flex;flex-wrap:wrap;gap:5px">
            <span class="badge b-b">💧{w["hum"]}%</span>
            <span class="badge b-b">🌧️{w["rp"]}%</span>
            <span class="badge b-b">💨{w["wind"]}km/h</span>
            <span class="badge b-b">🌡️{w["precip"]}mm</span>
          </div>
        </div>""", unsafe_allow_html=True)

        # City risk profile — read only, not editable
        cp = get_sliders(city)
        st.markdown('<div class="sec">📋 City Infrastructure Profile (Auto-loaded)</div>', unsafe_allow_html=True)
        factors = [
            ("🏗️ Infrastructure Quality", 10-cp["infrastructure"], "Higher = better"),
            ("🌊 Drainage Systems", 10-cp["drainage"], "Higher = better"),
            ("🏛️ Disaster Preparedness", 10-cp["preparedness"], "Higher = better"),
            ("🏙️ Urbanization Pressure", cp["urbanization"], "Higher = more risk"),
            ("🌿 Deforestation Level", cp["deforestation"], "Higher = more risk"),
            ("🏔️ Geographic Risk", cp["topography"], "Higher = more risk"),
        ]
        for label, val, note in factors:
            bar_w = val * 10
            col_b = "#ef4444" if val>=7 else "#f59e0b" if val>=4 else "#10b981"
            st.markdown(f"""
            <div style="margin:6px 0">
              <div style="display:flex;justify-content:space-between;margin-bottom:3px">
                <span style="font-size:.8rem;color:#e8edf5">{label}</span>
                <span style="font-size:.75rem;color:#7a8ea8">{val}/10</span>
              </div>
              <div style="background:#1e2d45;border-radius:4px;height:6px">
                <div style="width:{bar_w}%;height:6px;border-radius:4px;background:{col_b}"></div>
              </div>
            </div>""", unsafe_allow_html=True)

    with col_r:
        prob = flood_risk(city, w)
        pct  = prob * 100
        if pct>=65:   col,label,emoji="#ef4444","HIGH RISK","🔴"
        elif pct>=40: col,label,emoji="#f59e0b","MEDIUM RISK","🟡"
        else:         col,label,emoji="#10b981","LOW RISK","🟢"

        # Plotly gauge
        if PLOTLY:
            st.plotly_chart(plotly_gauge(pct, f"Flood Risk — {city}", col), use_container_width=True)
        else:
            st.markdown(f'<div class="pred" style="border-color:{col}"><div class="pred-n" style="color:{col}">{pct:.1f}%</div><div style="color:{col}">{emoji} {label}</div></div>', unsafe_allow_html=True)

        heat = heat_risk(w, city)
        hl, hc, he = hlabel(heat)
        st.markdown(f"""
        <div style="background:#0d1421;border:1px solid #1e2d45;border-radius:10px;
                    padding:14px;margin:8px 0;display:flex;justify-content:space-between">
          <div>
            <div style="font-size:.7rem;color:#7a8ea8;text-transform:uppercase;letter-spacing:.08em">Heatwave Risk</div>
            <div style="font-family:monospace;font-size:1.5rem;color:{hc};font-weight:700">{heat:.0f}% {he}</div>
            <div style="font-size:.78rem;color:{hc}">{hl}</div>
          </div>
          <div style="text-align:right;font-size:.78rem;color:#7a8ea8">
            {w["temp"]}°C / feels {w["feels"]}°C<br>Humidity: {w["hum"]}%
          </div>
        </div>""", unsafe_allow_html=True)

        if label=="HIGH RISK":
            st.markdown(f'<div class="alert a-crit"><b>⚠️ IMMEDIATE ACTION — {city}</b><br>🚨 Issue flood warning · 🚧 Close low-lying roads<br>🏗️ Deploy pumps · 📢 Alert NDMA · 🏠 Begin evacuation</div>',unsafe_allow_html=True)
        elif label=="MEDIUM RISK":
            st.markdown(f'<div class="alert a-warn"><b>⚡ STAY ALERT — {city}</b><br>📡 Monitor rainfall · 🔍 Inspect drainage · 📋 Standby teams</div>',unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="alert a-ok"><b>✅ NORMAL — {city}</b><br>📊 Routine monitoring · 🌱 Maintain infrastructure</div>',unsafe_allow_html=True)

        if st.button("💾 Save Alert", type="primary"):
            db_flood(city, prob, label, w, heat)
            st.success("Saved!")


elif "Heatwave" in page:
    st.markdown("# 🌡️ Heatwave Alert Module")
    st.markdown("Real-time temperature monitoring — Pakistan faces extreme heat events up to 54°C")
    if season["w"]: st.markdown(f'<div class="alert a-info">{season["e"]} {season["w"]}</div>',unsafe_allow_html=True)

    # City Search
    st.markdown('<div class="sec">🔍 Search Any Pakistani City</div>', unsafe_allow_html=True)
    hs1, hs2 = st.columns([4,1])
    with hs1:
        heat_search = st.text_input("", placeholder="Search any city in Pakistan...", label_visibility="collapsed", key="heat_search")
    with hs2:
        heat_search_btn = st.button("Search 🔍", type="primary", use_container_width=True, key="heat_search_btn")

    if heat_search_btn and heat_search:
        with st.spinner(f"Fetching data for {heat_search}..."):
            hfound = search_pakistan_city(heat_search)
        if hfound["found"]:
            hw = get_weather_by_coords(hfound["lat"], hfound["lon"])
            hhs = heat_risk(hw, "Karachi")
            hhl, hhc, hhe = hlabel(hhs)
            st.markdown(f"""
            <div class="card" style="border-color:{hhc}">
              <div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px">
                <div>
                  <b style="color:{hhc};font-size:1.1rem">{hfound["name"]}</b>
                  <span style="color:#7a8ea8"> · {hfound["province"]}</span>
                </div>
                <div style="text-align:right">
                  {wemoji(hw["code"])} <b style="font-family:monospace;font-size:1.4rem;color:{hhc}">{hw["temp"]}°C</b>
                  <span style="color:#7a8ea8;font-size:.8rem"> / feels {hw["feels"]}°C</span>
                </div>
              </div>
              <div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:8px">
                <span class="badge b-b">💧 {hw["hum"]}%</span>
                <span class="badge b-b">💨 {hw["wind"]} km/h</span>
                <span class="badge {'b-r' if hhs>=70 else 'b-a' if hhs>=50 else 'b-g'}">{hhe} Heat {hhs:.0f}% — {hhl}</span>
              </div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="alert a-warn">⚠️ "{heat_search}" not found. Try different spelling.</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Load all city heat data
    with st.spinner("Loading live temperatures..."):
        heat_data=[]
        for cn,_ in CITIES.items():
            w=get_weather(cn); hs=heat_risk(w,cn); hl2,hc2,he2=hlabel(hs)
            heat_data.append({"city":cn,"temp":w["temp"],"feels":w["feels"],
                              "hum":w["hum"],"score":hs,"label":hl2,"color":hc2,"emoji":he2})
        heat_data.sort(key=lambda x:x["score"],reverse=True)

    top10_heat = heat_data[:10]

    # Top 10 Heatwave with Plotly
    st.markdown('<div class="sec">🏆 Top 10 Highest Heatwave Risk Cities — Right Now</div>', unsafe_allow_html=True)
    if PLOTLY:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=[d["score"] for d in reversed(top10_heat)],
            y=[d["city"] for d in reversed(top10_heat)],
            orientation="h",
            marker_color=[d["color"] for d in reversed(top10_heat)],
            text=[f"{d['temp']}°C · {d['score']:.0f}%" for d in reversed(top10_heat)],
            textposition="outside",
            textfont={"color":"#e8edf5","size":10}
        ))
        fig.add_vline(x=70,line_dash="dash",line_color="#ef4444",line_width=1)
        fig.add_vline(x=50,line_dash="dash",line_color="#f59e0b",line_width=1)
        fig.update_layout(
            title={"text":"Top 10 Heatwave Risk Cities","font":{"color":"#e8edf5","size":14}},
            paper_bgcolor="#080c14",plot_bgcolor="#0d1421",
            font={"color":"#7a8ea8"},
            xaxis={"range":[0,120],"gridcolor":"#1e2d45","color":"#7a8ea8","title":"Heat Risk Score"},
            yaxis={"gridcolor":"#1e2d45","color":"#e8edf5"},
            height=380,margin=dict(l=130,r=80,t=50,b=30)
        )
        st.plotly_chart(fig, use_container_width=True)

    # City cards grid
    st.markdown('<div class="sec">🌡️ All Cities — Live Temperature</div>', unsafe_allow_html=True)
    heat_grid = '<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:10px;margin:8px 0">'
    for d in heat_data:
        bc = "b-r" if d["score"]>=70 else "b-a" if d["score"]>=50 else "b-g"
        heat_grid += f"""
        <div class="card" style="border-color:{d["color"]}40;min-width:0">
          <b style="color:#e8edf5;font-size:.88rem">{d["city"]}</b><br>
          <span style="font-family:monospace;font-size:1.2rem;color:{d["color"]}">{d["temp"]}°C</span>
          <span style="font-size:.7rem;color:#7a8ea8"> /{d["feels"]}°C</span><br>
          <div class="prog-w" style="margin:5px 0">
            <div class="prog-f" style="width:{d["score"]}%;background:{d["color"]}"></div>
          </div>
          <span class="badge {bc}">{d["emoji"]} {d["label"]} {d["score"]:.0f}%</span>
        </div>"""
    heat_grid += "</div>"
    st.markdown(heat_grid, unsafe_allow_html=True)

    # Detailed city analysis
    st.markdown("---")
    st.markdown('<div class="sec">🔬 Detailed City Analysis</div>', unsafe_allow_html=True)
    sel = st.selectbox("Select City for Details", list(CITIES.keys()))
    w = get_weather(sel); hs = heat_risk(w,sel); hl,hc,he = hlabel(hs)
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("Temperature", f"{w['temp']}°C")
    with c2: st.metric("Feels Like",  f"{w['feels']}°C")
    with c3: st.metric("Humidity",    f"{w['hum']}%")
    with c4: st.metric("Heat Risk",   f"{hs:.0f}%", hl)

    if PLOTLY:
        st.plotly_chart(plotly_gauge(hs, f"Heatwave Risk — {sel}", hc), use_container_width=True)

    if hl in ["EXTREME","HIGH"]:
        st.markdown(f'<div class="alert a-crit"><b>🌡️ {hl} HEATWAVE — {sel}</b><br>⚕️ Open cooling centers · 🏥 Alert hospitals · 🚰 Distribute water<br>⛔ Restrict outdoor work 11am–4pm · 👴 Prioritize vulnerable groups</div>',unsafe_allow_html=True)
    elif hl=="MODERATE":
        st.markdown(f'<div class="alert a-warn"><b>⚠️ MODERATE HEAT — {sel}</b><br>💧 Encourage hydration · 🌳 Shade recommendations · 📢 Public awareness</div>',unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="alert a-ok"><b>✅ LOW HEAT RISK — {sel}</b><br>Normal conditions. Routine monitoring.</div>',unsafe_allow_html=True)

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

