import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
        
        .stApp {
            background-color: #0B0E14;
            color: #FAFAFA;
            font-family: 'Outfit', sans-serif;
        }
        .main-header {
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 2rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            animation: fadeIn 1s ease-in;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .status-healthy, .status-warning, .status-critical {
            padding: 1.2rem;
            border-radius: 12px;
            text-align: center;
            font-weight: 800;
            font-size: 1.8rem;
            letter-spacing: 1px;
            backdrop-filter: blur(10px);
            margin-bottom: 1rem;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        }
        
        .status-healthy {
            background-color: rgba(46, 204, 113, 0.15);
            color: #2ecc71;
            border: 1px solid rgba(46, 204, 113, 0.3);
        }
        .status-warning {
            background-color: rgba(241, 196, 15, 0.15);
            color: #f1c40f;
            border: 1px solid rgba(241, 196, 15, 0.3);
        }
        .status-critical {
            background-color: rgba(231, 76, 60, 0.15);
            color: #e74c3c;
            border: 1px solid rgba(231, 76, 60, 0.5);
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(231, 76, 60, 0.4); }
            70% { box-shadow: 0 0 0 20px rgba(231, 76, 60, 0); }
            100% { box-shadow: 0 0 0 0 rgba(231, 76, 60, 0); }
        }
        
        .metric-card {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(16px);
            padding: 1.5rem;
            border-radius: 16px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-top: 4px solid #00C9FF;
            transition: all 0.3s ease;
        }
        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.4);
            border-top: 4px solid #92FE9D;
            background: rgba(255, 255, 255, 0.05);
        }
        .metric-value {
            font-size: 3.5rem;
            font-weight: 800;
            color: #FFFFFF;
            line-height: 1.2;
            text-shadow: 0 0 10px rgba(255,255,255,0.2);
        }
        .metric-label {
            font-size: 1.1rem;
            color: #A0AAB5;
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 1px;
            margin-top: 0.5rem;
        }
        </style>
    """, unsafe_allow_html=True)

def render_health_status(rul: float, warning_threshold: int = 50, critical_threshold: int = 20):
    if rul > warning_threshold:
        st.markdown('<div class="status-healthy">✨ HEALTHY</div>', unsafe_allow_html=True)
        st.info(f"Engine is operating nominally. Estimated {int(rul)} cycles remaining.")
    elif rul > critical_threshold:
        st.markdown('<div class="status-warning">⚠️ WARNING</div>', unsafe_allow_html=True)
        st.warning(f"Engine degradation detected. Maintenance recommended in {int(rul)} cycles.")
    else:
        st.markdown('<div class="status-critical">🚨 CRITICAL</div>', unsafe_allow_html=True)
        st.error(f"Imminent failure risk! Immediate maintenance required. Estimated {int(rul)} cycles remaining.")
