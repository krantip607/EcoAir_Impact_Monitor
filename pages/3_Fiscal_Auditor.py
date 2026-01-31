import streamlit as st
import plotly.graph_objects as go
import sys
import os

# Link to core engine
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engines import calculate_fiscal_loss

st.set_page_config(page_title="Fiscal Auditor", layout="wide")

# --- HIGH-VISIBILITY FINANCIAL STYLING ---
st.markdown("""
    <style>
    .stApp { background: #050505; color: white; }
    .money-card {
        background: rgba(255, 191, 0, 0.05);
        border: 2px solid #FFBF00;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 0 25px rgba(255, 191, 0, 0.2);
    }
    h1, h2, h3 { color: #FFBF00; text-shadow: 0 0 10px rgba(255, 191, 0, 0.5); }
    [data-testid="stMetricValue"] { color: #FFBF00 !important; font-size: 3rem !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("💰 FISCAL IMPACT & PRODUCTIVITY AUDITOR")

# Check for Shared Memory
if 'city_data' in st.session_state and st.session_state['city_data'] is not None:
    data = st.session_state['city_data']
    aqi = data.get('aqi', 0)
    
    # Calculate Loss (Assuming 12M population and $15 avg hourly wage for the city)
    hourly_loss = calculate_fiscal_loss(12000000, 15, aqi)
    annual_projection = hourly_loss * 8 * 260 # 8 hours/day, 260 work days

    st.markdown(f"### LIVE ECONOMY AUDIT: {data['name'].upper()}")
    
    # --- ROW 1: THE MONEY LEAK CARD ---
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        # Productivity Loss Gauge
        fig = go.Figure(go.Indicator(
            mode = "number+delta",
            value = hourly_loss,
            number = {'prefix': "$", 'valueformat': ",.0f"},
            delta = {'reference': 0, 'relative': False, 'increasing': {'color': "#FFBF00"}},
            title = {'text': "Hourly Productivity Leakage", 'font': {'color': "#FFBF00", 'size': 20}}
        ))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, height=300)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.write("## ") # Spacer
        st.markdown(f"""
            <div class="money-card">
                <p style="margin:0; color:#888;">PROJECTED ANNUAL DRAIN</p>
                <h1 style="margin:10px 0;">${annual_projection/1e6:.1f}M</h1>
                <p style="color:#ccc;">Estimated GDP impact due to pollution-linked labor inefficiency in {data['name']}.</p>
            </div>
        """, unsafe_allow_html=True)

    # --- ROW 2: ECONOMIC DECAY CHART ---
    st.markdown("---")
    st.subheader("📉 The 'Invisible' GDP Tax (AQI vs. Efficiency)")
    
    # Chart showing how productivity drops as AQI rises
    aqi_range = list(range(0, 401, 50))
    efficiency = [100 - (0.05 * x if x > 100 else 0) for x in aqi_range]
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=aqi_range, y=efficiency, fill='tozeroy',
                             line=dict(color='#FFBF00', width=4),
                             fillcolor='rgba(255, 191, 0, 0.1)'))
    
    # Highlight current city position
    fig2.add_vline(x=aqi, line_dash="dash", line_color="red", annotation_text="Current City Status")
    
    fig2.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "white"},
        xaxis_title="Air Quality Index (AQI)",
        yaxis_title="Worker Efficiency (%)",
        yaxis=dict(range=[70, 105], gridcolor='#333'),
        xaxis=dict(showgrid=False)
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    st.info("Audit Logic: Correlation between high AQI and cognitive/physical labor productivity decline.")

else:
    st.warning("⚠️ AUDIT STANDBY: Please enter your Token and City on the Main Page first.")