import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from engines import calculate_bio_risk, calculate_fiscal_loss
from api_helper import get_live_data

# --- 1. PAGE CONFIGURATION & MEMORY INITIALIZATION ---
st.set_page_config(page_title="ImpactAir Terminal", layout="wide")

# Initialize memory (Session State) so it doesn't reset on page change
if 'token' not in st.session_state:
    st.session_state['token'] = ""
if 'city' not in st.session_state:
    st.session_state['city'] = "Mumbai"
if 'city_data' not in st.session_state:
    st.session_state['city_data'] = None

# --- 2. HIGH-VISIBILITY CSS ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #050505 0%, #0a0a12 100%); color: #FFFFFF; }
    [data-testid="metric-container"] {
        background: rgba(0, 0, 0, 0.7);
        border: 2px solid #00FF41;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.2);
    }
    [data-testid="stMetricValue"] { color: #00FF41 !important; font-family: 'Courier New', monospace; font-size: 2.5rem !important; }
    [data-testid="stMetricLabel"] { color: #FFFFFF !important; font-weight: bold !important; }
    section[data-testid="stSidebar"] { background-color: #000000; border-right: 2px solid #00FF41; }
    h1 { color: #00FF41; text-shadow: 2px 2px 10px rgba(0, 255, 65, 0.5); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR: PERSISTENT INPUTS ---
st.sidebar.title("📡 AUDIT CONTROL")

# These inputs now link directly to Session State
st.session_state['city'] = st.sidebar.text_input("📍 TARGET CITY", value=st.session_state['city'])
st.session_state['token'] = st.sidebar.text_input("🔑 API TOKEN", value=st.session_state['token'], type="password")

# Button to manually refresh or change data
if st.sidebar.button("🔄 RE-SYNC AUDIT"):
    st.session_state['city_data'] = get_live_data(st.session_state['city'], st.session_state['token'])

# --- 4. DATA LOGIC ---
st.title("🏙️ IMPACTAIR: BIO-ECONOMIC AUDITOR")

# Only fetch data if we don't have it yet, or if user explicitly asks
if st.session_state['token'] and st.session_state['city']:
    if st.session_state['city_data'] is None:
        st.session_state['city_data'] = get_live_data(st.session_state['city'], st.session_state['token'])
    
    data = st.session_state['city_data']
    
    if data:
        st.sidebar.success(f"ACTIVE: {data['name']}")
        
        # Calculations using engines.py
        dose, cigs = calculate_bio_risk(data['pm25'], 25, "Active")
        loss = calculate_fiscal_loss(12000000, 15, data['aqi'])
        
        # Top KPI Metrics
        st.subheader(f"AUDIT SUMMARY: {data['name'].upper()}")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("BIOLOGICAL LOAD", f"{dose}μg", delta=f"{cigs} cigs/day", delta_color="inverse")
        with c2:
            st.metric("FISCAL LEAKAGE", f"${loss:,.0f}", delta="HOURLY LOSS", delta_color="inverse")
        with c3:
            st.metric("AIR QUALITY (AQI)", data['aqi'], delta="LIVE FEED")

        # Visual Chart
        st.markdown("---")
        st.subheader("📊 PROJECTED PRODUCTIVITY DECAY")
        df = pd.DataFrame({
            'Hour': list(range(24)),
            'Loss ($)': [loss * (1 + 0.1 * np.random.randn()) for _ in range(24)]
        })
        fig = px.area(df, x='Hour', y='Loss ($)', template="plotly_dark", color_discrete_sequence=['#00FF41'])
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.error("❌ ERROR: Data could not be retrieved. Check Token or City Name.")
else:
    st.warning("⚠️ SYSTEM STANDBY: Please enter Credentials in the Sidebar to begin.")