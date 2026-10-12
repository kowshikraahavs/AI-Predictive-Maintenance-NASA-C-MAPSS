import joblib
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV
from src.utils.config import MODELS_DIR, RANDOM_STATE, FAST_MODE
from src.utils.logging_utils import get_logger

logger = get_logger(__name__)

def train_random_forest(X_train, y_train):
    """
    Trains a Random Forest Regression model.
    """
    logger.info("Training Random Forest Model...")
    
    rf = RandomForestRegressor(random_state=RANDOM_STATE, n_jobs=-1)
    
    if FAST_MODE:
        param_distributions = {
            'n_estimators': [50, 100],
            'max_depth': [5, 10]
        }
        n_iter = 2
    else:
        param_distributions = {
            'n_estimators': [100, 200],
            'max_depth': [10, 20, None],
            'min_samples_split': [2, 5],
            'min_samples_leaf': [1, 2]
        }
        n_iter = 5
        
    random_search = RandomizedSearchCV(
        estimator=rf,
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
    
    logger.info(f"Best RF Params: {random_search.best_params_}")
    
    # Save model
    model_path = os.path.join(MODELS_DIR, "rf_model.joblib")
    joblib.dump(best_model, model_path)
    logger.info(f"Random Forest model saved to {model_path}")
    
    return best_model
