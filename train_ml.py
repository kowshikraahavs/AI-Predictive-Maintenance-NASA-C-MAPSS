import os
import pandas as pd
import json
from src.utils.logging_utils import get_logger
from src.utils.config import PROCESSED_DATA_DIR, MODELS_DIR
from src.models.baseline import train_baseline
from src.models.random_forest import train_random_forest
from src.models.xgboost_model import train_xgboost
from src.evaluation.metrics import evaluate_model

logger = get_logger(__name__)

def run_ml_training():
    logger.info("Starting ML model training pipeline...")
    
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
            
        # Get X and y
        X_train = train_df[feature_cols]
        y_train = train_df['RUL']
        
        # For evaluation, we typically evaluate on the LAST cycle of each test engine
        test_last_cycle = test_df.groupby('unit_id').last().reset_index()
        X_test = test_last_cycle[feature_cols]
        y_test = test_last_cycle['RUL']
        
        # Train and Evaluate Baseline
        baseline_model = train_baseline(X_train, y_train)
        y_pred_base = baseline_model.predict(X_test)
        metrics_base = evaluate_model(y_test, y_pred_base, "Baseline (Linear Regression)")
        
        # Train and Evaluate Random Forest
        rf_model = train_random_forest(X_train, y_train)
        y_pred_rf = rf_model.predict(X_test)
        metrics_rf = evaluate_model(y_test, y_pred_rf, "Random Forest")
        
        # Train and Evaluate XGBoost
        xgb_model = train_xgboost(X_train, y_train)
        y_pred_xgb = xgb_model.predict(X_test)
        metrics_xgb = evaluate_model(y_test, y_pred_xgb, "Gradient Boosting")
        
        # Save metrics
        all_metrics = {
            "Linear Regression": metrics_base,
            "Random Forest": metrics_rf,
            "Gradient Boosting": metrics_xgb
        }
        
        metrics_path = os.path.join(MODELS_DIR, "ml_metrics.json")
        with open(metrics_path, "w") as f:
            json.dump(all_metrics, f, indent=4)
            
        logger.info(f"ML Metrics saved to {metrics_path}")
        
    except Exception as e:
        logger.error(f"ML training failed: {str(e)}")

if __name__ == "__main__":
    run_ml_training()
