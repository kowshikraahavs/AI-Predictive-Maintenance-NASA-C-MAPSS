import joblib
import os
from sklearn.linear_model import LinearRegression
from src.utils.config import MODELS_DIR
from src.utils.logging_utils import get_logger

logger = get_logger(__name__)

def train_baseline(X_train, y_train):
    """
    Trains a simple Linear Regression model as a baseline.
    """
    logger.info("Training Baseline Model (Linear Regression)...")
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Save model
    model_path = os.path.join(MODELS_DIR, "baseline_model.joblib")
    joblib.dump(model, model_path)
    logger.info(f"Baseline model saved to {model_path}")
    
    return model
