import streamlit as st
import plotly.graph_objects as go
import sys
import os

# Link to core engine
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engines import calculate_bio_risk

st.set_page_config(page_title="Biological Auditor", layout="wide")

# --- HIGH-VISIBILITY BIOLOGICAL STYLING ---
st.markdown("""
    <style>
    .stApp { background: #050505; color: white; }
    .bio-card {
        background: rgba(255, 75, 75, 0.05);
        border: 2px solid #ff4b4b;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 0 20px rgba(255, 75, 75, 0.2);
    }
    h1, h2, h3 { color: #ff4b4b; text-shadow: 0 0 12px rgba(255, 75, 75, 0.6); }
    [data-testid="stMetricValue"] { color: #ff4b4b !important; font-size: 3rem !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🫁 BIOLOGICAL & RESPIRATORY AUDITOR")

# Check for Session Memory
if 'city_data' in st.session_state and st.session_state['city_data'] is not None:
    data = st.session_state['city_data']
    pm25 = data.get('pm25', 0)
    
    # Calculate Impact (Assuming Average Age 30 and Active Level for Audit)
    dose, cigs = calculate_bio_risk(pm25, 30, "Active")

    st.markdown(f"### LIVE AUDIT: {data['name'].upper()}")
    
    # --- ROW 1: THE GAUGE AND THE CIGARETTE EQUIVALENT ---
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # PM2.5 Exposure Gauge
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = pm25,
            title = {'text': "Atmospheric PM2.5 (μg/m³)", 'font': {'color': "#ff4b4b", 'size': 20}},
            gauge = {
                'axis': {'range': [0, 500], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': "#ff4b4b"},
                'steps': [
                    {'range': [0, 50], 'color': "rgba(0, 255, 65, 0.1)"},
                    {'range': [50, 150], 'color': "rgba(255, 255, 0, 0.1)"},
                    {'range': [150, 500], 'color': "rgba(255, 75, 75, 0.2)"}
                ],
            }
        ))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.write("## ") # Spacer
        st.markdown(f"""
            <div class="bio-card">
                <p style="margin:0; color:#888;">DAILY DAMAGE EQUIVALENT</p>
                <h1 style="margin:10px 0;">{cigs}</h1>
                <h3 style="margin:0;">CIGARETTES</h3>
                <p style="color:#ccc; margin-top:10px;">Calculated biological toll on lung tissue based on {pm25}μg concentration.</p>
            </div>
        """, unsafe_allow_html=True)

    # --- ROW 2: TISSUE DEPOSITION GRAPH ---
    st.markdown("---")
    st.subheader("🩸 Hourly Particulate Deposition Projection")
    
    # Simple line chart showing inhaled dose over time
    hours = list(range(1, 13))
    cumulative_dose = [dose * h for h in hours]
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=hours, y=cumulative_dose, mode='lines+markers', 
                             line=dict(color='#ff4b4b', width=4),
                             fill='tozeroy', fillcolor='rgba(255, 75, 75, 0.1)'))
    
    fig2.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "white"},
        xaxis_title="Hours of Outdoor Exposure",
        yaxis_title="Inhaled Dose (μg)",
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor='#333')
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    st.info("Audit Logic: Translating particulate concentration into physiological tissue load.")
    st.markdown("---")
        st.subheader("📢 AI Auditor Recommendation")
        if pm25 > 35:
            st.error("🚨 **High Alert:** Reduce outdoor activity. Authorities should consider traffic restrictions to lower PM2.5 levels.")
        else:
            st.success("✅ **Safe Zone:** Air quality is within acceptable biological limits for most individuals.")

else:
    st.warning("⚠️ AUDIT STANDBY: Please enter your Token and City on the Main Page first.")
