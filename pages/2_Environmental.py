import streamlit as st
import plotly.graph_objects as go
import sys
import os

# Link to core engine
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engines import calculate_environmental_decay

st.set_page_config(page_title="Structural Auditor", layout="wide")

# --- HIGH-VISIBILITY CYBER STYLING ---
st.markdown("""
    <style>
    .stApp { background: #050505; color: white; }
    .status-card {
        background: rgba(0, 255, 65, 0.05);
        border: 2px solid #00FF41;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
    }
    h1, h2, h3 { color: #00FF41; text-shadow: 0 0 10px rgba(0, 255, 65, 0.5); }
    </style>
    """, unsafe_allow_html=True)

st.title("🏗️ ENVIRONMENTAL & STRUCTURAL AUDITOR")

# Check for Session Memory
if 'city_data' in st.session_state and st.session_state['city_data'] is not None:
    data = st.session_state['city_data']
    so2 = data.get('so2', 0)
    humidity = data.get('humidity', 0)
    status, multiplier = calculate_environmental_decay(so2, humidity)

    st.markdown(f"### LIVE AUDIT: {data['name'].upper()}")
    
    # --- ROW 1: GAUGE AND STATUS ---
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Corrosion Velocity Gauge
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = multiplier,
            title = {'text': "Corrosion Multiplier (Velocity)", 'font': {'color': "#00FF41", 'size': 20}},
            gauge = {
                'axis': {'range': [1, 5], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': "#ff4b4b" if multiplier > 1 else "#00FF41"},
                'steps': [
                    {'range': [1, 2], 'color': "rgba(0, 255, 65, 0.2)"},
                    {'range': [2, 5], 'color': "rgba(255, 75, 75, 0.2)"}
                ],
            }
        ))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, height=350)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.write("## ") # Spacer
        color = "#ff4b4b" if status == "CRITICAL" else "#00FF41"
        st.markdown(f"""
            <div class="status-card" style="border-color: {color};">
                <p style="margin:0; color:#888;">CURRENT STATUS</p>
                <h1 style="color: {color}; margin:10px 0;">{status}</h1>
                <p style="color:#ccc;">⚠ Accelerated material degradation detected in {data['name']}.</p>
            </div>
        """, unsafe_allow_html=True)

    # --- ROW 2: LIFESPAN COMPARISON ---
    st.markdown("---")
    st.subheader("📉 Projected Infrastructure Lifespan Reduction")
    
    # Comparison Chart: Standard vs Corrosive Environment
    components = ['Steel Beam', 'Concrete Foundation', 'Limestone Facade']
    standard_life = [50, 80, 100]
    impacted_life = [life / multiplier for life in standard_life]

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(name='Normal Environment', x=components, y=standard_life, marker_color='#333'))
    fig2.add_trace(go.Bar(name=f"Current Environment ({data['name']})", x=components, y=impacted_life, marker_color='#00FF41'))
    
    fig2.update_layout(
        barmode='group', 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "white"},
        yaxis_title="Estimated Years Until Failure"
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    st.info("Logic Source: ISO 9223 Standard mapping for atmospheric corrosivity")

else:
    st.warning("⚠️ AUDIT STANDBY: Please enter your Token and City on the Main Page first.")