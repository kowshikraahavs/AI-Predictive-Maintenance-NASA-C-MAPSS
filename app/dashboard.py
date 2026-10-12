import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
import plotly.graph_objects as go

# Add project root to path so we can import src modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.config import PROCESSED_DATA_DIR, RAW_DATA_DIR
from src.inference.predictor import RULPredictor
from app.components.ui_utils import apply_custom_css, render_health_status

st.set_page_config(page_title="Turbofan RUL Predictor", page_icon="✈️", layout="wide", initial_sidebar_state="expanded")
apply_custom_css()

st.markdown('<div class="main-header">AI Engine Health & RUL Predictor</div>', unsafe_allow_html=True)

@st.cache_resource
def load_data():
    try:
        test_df = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, "test_processed.csv"))
        return test_df
    except FileNotFoundError:
        return None

test_df = load_data()

if test_df is None:
    st.error("Processed data not found. Please run the preprocessing and training pipelines first.")
    st.stop()

# Configuration in Sidebar
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    model_choice = st.selectbox(
        "Prediction Model",
        ["LSTM", "Gradient Boosting", "Random Forest", "Linear Regression"]
    )
    
try:
    predictor = RULPredictor(model_type=model_choice)
except Exception as e:
    st.error(f"Failed to load {model_choice} model. Error: {str(e)}")
    st.stop()

tab1, tab2 = st.tabs(["🚀 Simulator (Test Dataset)", "📂 Custom Sensor Log Upload"])

with tab1:
    st.markdown("### 🕹️ Simulation Control")
    col1, col2 = st.columns([1, 2])
    with col1:
        engine_ids = test_df['unit_id'].unique()
        selected_engine = st.selectbox("Select Engine (Unit ID)", engine_ids)
        
        engine_data = test_df[test_df['unit_id'] == selected_engine].copy()
        max_cycle = int(engine_data['cycle'].max())
        
        selected_cycle = st.slider("Current Operating Cycle", min_value=1, max_value=max_cycle, value=max_cycle)

    with col2:
        history_df = engine_data[engine_data['cycle'] <= selected_cycle]
        predicted_rul = predictor.predict(history_df)

        true_rul_row = history_df.iloc[-1]
        true_rul = true_rul_row['RUL'] if 'RUL' in true_rul_row else None

        m1, m2, m3 = st.columns(3)

        with m1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{int(predicted_rul)}</div>
                    <div class="metric-label">Predicted RUL</div>
                </div>
            """, unsafe_allow_html=True)
            
        with m2:
            val = int(true_rul) if true_rul is not None else "N/A"
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{val}</div>
                    <div class="metric-label">Actual RUL</div>
                </div>
            """, unsafe_allow_html=True)
                
        with m3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{selected_cycle}</div>
                    <div class="metric-label">Current Cycle</div>
                </div>
            """, unsafe_allow_html=True)
            
    st.markdown("<br>", unsafe_allow_html=True)
    render_health_status(predicted_rul)
    st.markdown("<br>", unsafe_allow_html=True)

    # Interactive Plotly Chart
    st.markdown("### 📈 Interactive Degradation Curve")

    fig = go.Figure()

    # True degradation
    fig.add_trace(go.Scatter(
        x=engine_data['cycle'], 
        y=engine_data['RUL'],
        mode='lines',
        name='True Degradation Profile',
        line=dict(color='#2ecc71', width=3)
    ))

    # Prediction point
    fig.add_trace(go.Scatter(
        x=[selected_cycle], 
        y=[predicted_rul],
        mode='markers',
        name='Current Prediction',
        marker=dict(color='#00C9FF', size=16, symbol='diamond', line=dict(color='#FFF', width=2))
    ))

    # Predicted trajectory
    predicted_failure_cycle = selected_cycle + predicted_rul
    fig.add_trace(go.Scatter(
        x=[selected_cycle, predicted_failure_cycle], 
        y=[predicted_rul, 0],
        mode='lines',
        name='Predicted Trajectory',
        line=dict(color='#00C9FF', width=3, dash='dash')
    ))

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FAFAFA', family="Outfit, sans-serif"),
        xaxis=dict(title='Operating Cycle', showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(title='Remaining Useful Life (Cycles)', showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=0, r=0, t=50, b=0),
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("### 📂 Upload Real-Time Sensor Logs")
    st.markdown("Upload a CSV file containing raw sensor telemetry data. The AI will automatically clean, scale, and feature-engineer the data before predicting the Remaining Useful Life.")
    
    uploaded_file = st.file_uploader("Upload Engine Data (CSV)", type=['csv'])
    
    if uploaded_file is not None:
        try:
            raw_data = pd.read_csv(uploaded_file)
            st.success("File uploaded successfully!")
            
            with st.spinner("Processing telemetry and running AI inference..."):
                processed_df = predictor.process_raw_data(raw_data)
                pred_rul_custom = predictor.predict(processed_df)
                
            st.markdown("---")
            m1, m2 = st.columns(2)
            
            with m1:
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{int(pred_rul_custom)}</div>
                        <div class="metric-label">Predicted RUL (Cycles)</div>
                    </div>
                """, unsafe_allow_html=True)
                
            with m2:
                current_cycle = processed_df['cycle'].max() if 'cycle' in processed_df.columns else len(processed_df)
                st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{int(current_cycle)}</div>
                        <div class="metric-label">Total Cycles In Log</div>
                    </div>
                """, unsafe_allow_html=True)
                
            st.markdown("<br>", unsafe_allow_html=True)
            render_health_status(pred_rul_custom)
            
            with st.expander("View Processed Data Summary"):
                st.dataframe(processed_df.tail(5))
                
        except Exception as e:
            st.error(f"Error processing the file: {str(e)}")
            st.warning("Ensure the CSV has the standard 21 sensor columns (e.g., 'sensor_1', 'sensor_2')")
