import joblib
import os
from sklearn.model_selection import RandomizedSearchCV
from src.utils.config import MODELS_DIR, RANDOM_STATE, FAST_MODE
from src.utils.logging_utils import get_logger

logger = get_logger(__name__)

def train_xgboost(X_train, y_train):
    """
    Trains an XGBoost model. Falls back to HistGradientBoostingRegressor if xgboost is not available.
    """
    logger.info("Training Gradient Boosting Model...")
    
    try:
        from xgboost import XGBRegressor
        logger.info("Using XGBoost Regressor.")
        model = XGBRegressor(random_state=RANDOM_STATE, n_jobs=-1, objective='reg:squarederror')
        
        if FAST_MODE:
            param_distributions = {
                'n_estimators': [50, 100],
                'max_depth': [3, 5],
                'learning_rate': [0.1, 0.2]
            }
            n_iter = 2
        else:
            param_distributions = {
                'n_estimators': [100, 200],
                'max_depth': [3, 5, 7],
                'learning_rate': [0.01, 0.1, 0.2],
                'subsample': [0.8, 1.0]
            }
            n_iter = 5
            
    except ImportError:
        logger.warning("XGBoost not installed. Falling back to HistGradientBoostingRegressor.")
        from sklearn.ensemble import HistGradientBoostingRegressor
        model = HistGradientBoostingRegressor(random_state=RANDOM_STATE)
        
        if FAST_MODE:
            param_distributions = {
                'max_iter': [50, 100],
                'max_depth': [3, 5],
                'learning_rate': [0.1]
            }
            n_iter = 2
        else:
            param_distributions = {
                'max_iter': [100, 200],
                'max_depth': [3, 5, 7],
                'learning_rate': [0.01, 0.1, 0.2]
            }
            n_iter = 5
            
    random_search = RandomizedSearchCV(
        estimator=model,
        param_distributions=param_distributions,
        n_iter=n_iter,
        cv=3,
        scoring='neg_mean_squared_error',
        random_state=RANDOM_STATE,
        n_jobs=-1,
        verbose=1
    )
    
    random_search.fit(X_train, y_train)
    best_model = random_search.best_estimator_
    
    logger.info(f"Best Boosting Params: {random_search.best_params_}")
    
    # Save model
    model_path = os.path.join(MODELS_DIR, "xgb_model.joblib")
    joblib.dump(best_model, model_path)
    logger.info(f"Boosting model saved to {model_path}")
    
    return best_model
