import pandas as pd
import json
import os
from src.utils.config import MODELS_DIR
from src.utils.logging_utils import get_logger

logger = get_logger(__name__)

def identify_constant_features(train_df: pd.DataFrame, feature_cols: list) -> list:
    """
    Identifies features that are constant or near-constant across the training dataset.
    """
    logger.info("Identifying constant features...")
    
    constant_features = []
    for col in feature_cols:
        # Check if standard deviation is zero (or very close to zero)
        if train_df[col].std() < 1e-4:
            constant_features.append(col)
            
    logger.info(f"Found {len(constant_features)} constant features: {constant_features}")
    return constant_features

def select_features(train_df: pd.DataFrame, test_df: pd.DataFrame, feature_cols: list) -> tuple:
    """
    Selects the useful features by removing constant ones.
    Saves the selected features list for inference.
    """
    constant_features = identify_constant_features(train_df, feature_cols)
    
    selected_features = [col for col in feature_cols if col not in constant_features]
    
    # Save the selected features list
    feature_config_path = os.path.join(MODELS_DIR, "selected_features.json")
    with open(feature_config_path, "w") as f:
        json.dump(selected_features, f)
        
    logger.info(f"Selected {len(selected_features)} features. Dropped {len(constant_features)}.")
    logger.info(f"Selected features saved to {feature_config_path}")
    
    return selected_features
