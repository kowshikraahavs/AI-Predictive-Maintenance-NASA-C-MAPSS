import os
import pandas as pd
import json
import numpy as np
from src.utils.logging_utils import get_logger
from src.utils.config import PROCESSED_DATA_DIR, MODELS_DIR, SEQUENCE_LENGTH, BATCH_SIZE, EPOCHS, FAST_MODE
from src.features.engineering import generate_sequences, get_last_sequence_per_unit
from src.models.lstm import train_lstm_model
from src.evaluation.metrics import evaluate_model
from sklearn.model_selection import train_test_split

logger = get_logger(__name__)

def run_lstm_training():
    logger.info("Starting LSTM model training pipeline...")
    
    try:
        # Load processed data
        train_df = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, "train_processed.csv"))
        test_df = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, "test_processed.csv"))
        
        # Load selected features config
        with open(os.path.join(MODELS_DIR, "selected_features.json"), "r") as f:
            base_features = json.load(f)
            
        feature_cols = base_features.copy()
        for col in base_features:
            feature_cols.append(f"{col}_roll_mean")
            feature_cols.append(f"{col}_roll_std")
            
        # Generate Sequences
        X, y = generate_sequences(train_df, SEQUENCE_LENGTH, feature_cols)
        
        if len(X) == 0:
            logger.error("No sequences generated. Check sequence length and data.")
            return
            
        # Split into train/validation (80/20)
        # Note: Proper way is to split by engine, but for simplicity we use train_test_split here
        # since sequences are independent at this point. In a strict setup, split units before sequences.
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Test Data: We evaluate on the last sequence of each test unit
        X_test, y_test = get_last_sequence_per_unit(test_df, SEQUENCE_LENGTH, feature_cols)
        
        # Train Model
        epochs = 5 if FAST_MODE else EPOCHS
        model = train_lstm_model(X_train, y_train, X_val, y_val, batch_size=BATCH_SIZE, epochs=epochs)
        
        # Evaluate Model
        logger.info("Evaluating LSTM model on test data...")
        model.eval()
        import torch
        with torch.no_grad():
            y_pred = model(torch.tensor(X_test, dtype=torch.float32)).numpy()
        y_pred = y_pred.flatten()
        
        metrics = evaluate_model(y_test, y_pred, "LSTM")
        
        # Save metrics
        metrics_path = os.path.join(MODELS_DIR, "ml_metrics.json")
        if os.path.exists(metrics_path):
            with open(metrics_path, "r") as f:
                all_metrics = json.load(f)
        else:
            all_metrics = {}
            
        all_metrics["LSTM"] = metrics
        
        with open(metrics_path, "w") as f:
            json.dump(all_metrics, f, indent=4)
            
        logger.info(f"LSTM Metrics saved to {metrics_path}")
        
    except Exception as e:
        logger.error(f"LSTM training failed: {str(e)}")

if __name__ == "__main__":
    run_lstm_training()
