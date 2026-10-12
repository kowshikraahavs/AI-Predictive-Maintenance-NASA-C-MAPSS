import joblib
import json
import os
import numpy as np
import pandas as pd
from src.utils.config import MODELS_DIR, SEQUENCE_LENGTH
from src.utils.logging_utils import get_logger

logger = get_logger(__name__)

class RULPredictor:
    def __init__(self, model_type="Random Forest"):
        self.model_type = model_type
        self.scaler = None
        self.selected_features = None
        self.model = None
        self._load_artifacts()
        
    def _load_artifacts(self):
        try:
            # Load scaler
            self.scaler = joblib.load(os.path.join(MODELS_DIR, "scaler.joblib"))
            
            # Load features
            with open(os.path.join(MODELS_DIR, "selected_features.json"), "r") as f:
                base_features = json.load(f)
                
            self.selected_features = base_features.copy()
            for col in base_features:
                self.selected_features.append(f"{col}_roll_mean")
                self.selected_features.append(f"{col}_roll_std")
                
            # Load model
            if self.model_type == "Random Forest":
                self.model = joblib.load(os.path.join(MODELS_DIR, "rf_model.joblib"))
            elif self.model_type == "Linear Regression":
                self.model = joblib.load(os.path.join(MODELS_DIR, "baseline_model.joblib"))
            elif self.model_type == "Gradient Boosting":
                self.model = joblib.load(os.path.join(MODELS_DIR, "xgb_model.joblib"))
            elif self.model_type == "LSTM":
                import torch
                from src.models.lstm import LSTMModel
                
                input_size = len(self.selected_features)
                self.model = LSTMModel(input_size=input_size)
                self.model.load_state_dict(torch.load(os.path.join(MODELS_DIR, "lstm_model.pt")))
                self.model.eval()
            else:
                raise ValueError(f"Unknown model type: {self.model_type}")
                
            logger.info(f"{self.model_type} Predictor initialized.")
        except Exception as e:
            logger.error(f"Failed to load artifacts for {self.model_type}: {str(e)}")
            raise
            
    def predict(self, df_history: pd.DataFrame) -> float:
        """
        Predicts RUL for a single engine given its history up to the current cycle.
        df_history should be preprocessed (rolling features added, scaled).
        """
        if self.model_type == "LSTM":
            # Needs a sequence of SEQUENCE_LENGTH
            if len(df_history) < SEQUENCE_LENGTH:
                # Pad with zeros
                pad_size = SEQUENCE_LENGTH - len(df_history)
                data = df_history[self.selected_features].values
                data = np.pad(data, ((pad_size, 0), (0, 0)), 'constant', constant_values=0)
            else:
                data = df_history[self.selected_features].values[-SEQUENCE_LENGTH:]
                
            data = data.reshape(1, SEQUENCE_LENGTH, len(self.selected_features))
            import torch
            with torch.no_grad():
                pred = self.model(torch.tensor(data, dtype=torch.float32)).numpy()
            pred = pred.flatten()[0]
        else:
            # ML models use the last row
            data = df_history[self.selected_features].iloc[-1:].values
            pred = self.model.predict(data)[0]
            
        return max(0.0, float(pred))
        
    def process_raw_data(self, raw_df: pd.DataFrame) -> pd.DataFrame:
        """
        Takes raw sensor logs (CSV), adds rolling features, scales them, 
        and prepares them for prediction.
        """
        from src.features.engineering import add_rolling_features
        import copy
        
        # We need the original unrolled selected features list
        with open(os.path.join(MODELS_DIR, "selected_features.json"), "r") as f:
            base_features = json.load(f)
            
        # 1. Ensure required columns are present
        missing = [col for col in base_features if col not in raw_df.columns]
        if missing:
            raise ValueError(f"Missing required sensor columns in CSV: {missing}")
            
        # Ensure 'unit_id' exists for grouping, if not assume it's one engine
        if 'unit_id' not in raw_df.columns:
            raw_df['unit_id'] = 1
            
        # Ensure 'cycle' exists, if not generate it
        if 'cycle' not in raw_df.columns:
            raw_df['cycle'] = range(1, len(raw_df) + 1)
            
        # 2. Add rolling features
        processed_df = add_rolling_features(raw_df.copy(), base_features)
        
        # 3. Scale using the saved scaler
        # Temporarily suppress warnings as we only transform the selected features
        processed_df[self.selected_features] = self.scaler.transform(processed_df[self.selected_features])
        
        return processed_df
