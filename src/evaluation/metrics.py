import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from src.utils.logging_utils import get_logger

logger = get_logger(__name__)

def evaluate_model(y_true, y_pred, model_name: str) -> dict:
    """
    Calculates evaluation metrics for RUL prediction.
    """
    # RUL cannot be negative, so we clip predictions below 0 to 0
    y_pred_clipped = np.clip(y_pred, a_min=0, a_max=None)
    
    mae = mean_absolute_error(y_true, y_pred_clipped)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred_clipped))
    r2 = r2_score(y_true, y_pred_clipped)
    
    metrics = {
        "MAE": round(mae, 4),
        "RMSE": round(rmse, 4),
        "R2": round(r2, 4)
    }
    
    logger.info(f"{model_name} Evaluation - MAE: {metrics['MAE']}, RMSE: {metrics['RMSE']}, R2: {metrics['R2']}")
    return metrics
