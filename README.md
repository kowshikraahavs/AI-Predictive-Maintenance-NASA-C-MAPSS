# AI-Based Predictive Maintenance and Remaining Useful Life Prediction

## Problem Statement
Aircraft turbofan engines are critical components where unexpected failure can lead to catastrophic consequences. Maintenance is typically scheduled based on time or usage, which can be inefficient (replacing healthy parts) or risky (parts failing before schedule). Predictive Maintenance aims to estimate the Remaining Useful Life (RUL) of an engine based on its real-time sensor data, allowing for maintenance to be scheduled exactly when needed.

## Project Objectives
1. Build an end-to-end Machine Learning and Deep Learning pipeline to predict engine RUL.
2. Develop a baseline model and compare it with advanced ensemble methods (Random Forest, Gradient Boosting).
3. Implement a Deep Learning model (LSTM) to capture sequential degradation patterns.
4. Provide an interactive Streamlit dashboard for real-time monitoring and prediction.

## Dataset Information
The project uses the **NASA C-MAPSS (Commercial Modular Aero-Propulsion System Simulation) FD001** dataset.
It contains simulated run-to-failure degradation trajectories for a fleet of turbofan engines under a single operating condition.

### Dataset Download Instructions
Since this is a publicly available dataset, you must download it and place it in the project folder.
1. Download the NASA C-MAPSS dataset.
2. Place the following three files inside the `data/raw/` directory:
   - `train_FD001.txt`
   - `test_FD001.txt`
   - `RUL_FD001.txt`

*(If the dataset is missing, the application will alert you upon running the pipeline).*

## Project Architecture
- `data/`: Contains raw and processed data.
- `notebooks/`: Jupyter notebooks for exploratory analysis and model development.
- `src/`: Core Python modules for data loading, preprocessing, feature engineering, modeling, and inference.
- `app/`: Streamlit dashboard application.
- `models/saved/`: Serialized models, scalers, and feature configurations.
- `reports/`: Generated metrics and plots.

## Installation & Setup

### Python Setup (Local)
Ensure you have Python 3.9+ installed.
```bash
pip install -r requirements.txt
```

### Docker Setup
You can run the dashboard using Docker without installing local Python dependencies.
```bash
docker-compose up --build
```
Access the dashboard at `http://localhost:8501`.

## Project Workflow & Training Instructions
Follow these steps to train the models from scratch:

**1. Data Preprocessing & Validation**
This validates the dataset, generates RUL labels, selects features, and applies scaling.
```bash
python preprocess_pipeline.py
```

**2. Train Machine Learning Models**
Trains Linear Regression (Baseline), Random Forest, and Gradient Boosting.
```bash
python train_ml.py
```

**3. Train Deep Learning Model (LSTM)**
Trains the PyTorch LSTM model on generated time-series sequences.
```bash
python train_lstm.py
```

## Running the Dashboard
After training, you can launch the interactive dashboard to predict RUL and view degradation curves.
```bash
streamlit run app/dashboard.py
```

## Evaluation Metrics
The models are evaluated based on:
- **MAE (Mean Absolute Error):** Average absolute difference between predicted and actual RUL.
- **RMSE (Root Mean Squared Error):** Penalizes larger errors more heavily.
- **R² (R-Squared):** Proportion of variance explained by the model.

## Limitations & Future Improvements
- **Limitations:** The FD001 dataset simulates a single operating condition and fault mode. Real-world data is much more complex and noisy.
- **Future Improvements:** Extend the pipeline to FD002-FD004 datasets which include multiple operating conditions and fault modes. Implement Transformer-based architectures for potentially better sequential modeling.

## Troubleshooting
- **Missing Data Error:** Ensure `train_FD001.txt`, `test_FD001.txt`, and `RUL_FD001.txt` are exactly named and placed inside `data/raw/`.
- **Model Load Error:** Ensure you have run all three training scripts (`preprocess_pipeline.py`, `train_ml.py`, `train_lstm.py`) before starting the dashboard.
