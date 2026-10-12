import os
import pandas as pd
from src.utils.logging_utils import get_logger
from src.utils.config import SENSOR_COLUMNS, SETTING_COLUMNS, PROCESSED_DATA_DIR
from src.data.loader import load_data
from src.data.preprocessing import generate_train_rul, generate_test_rul, scale_features
from src.features.selection import select_features
from src.features.engineering import add_rolling_features

logger = get_logger(__name__)

def run_pipeline():
    logger.info("Starting preprocessing pipeline...")
    
    try:
        # 1. Load Data
        train_df, test_df, rul_df = load_data()
        
        # 2. Generate RUL
        train_df = generate_train_rul(train_df)
        test_df = generate_test_rul(test_df, rul_df)
        
        # 3. Feature Selection
        feature_cols = SETTING_COLUMNS + SENSOR_COLUMNS
        selected_features = select_features(train_df, test_df, feature_cols)
        
        # 4. Add Rolling Features
        train_df = add_rolling_features(train_df, selected_features)
        test_df = add_rolling_features(test_df, selected_features)
        
        # New feature columns after adding rolling features
        final_feature_cols = selected_features.copy()
        for col in selected_features:
            final_feature_cols.append(f"{col}_roll_mean")
            final_feature_cols.append(f"{col}_roll_std")
            
        # 5. Scale Features
        train_scaled, test_scaled, _ = scale_features(train_df, test_df, final_feature_cols)
        
        # 6. Save Processed Data
        train_scaled.to_csv(os.path.join(PROCESSED_DATA_DIR, "train_processed.csv"), index=False)
        test_scaled.to_csv(os.path.join(PROCESSED_DATA_DIR, "test_processed.csv"), index=False)
        
        logger.info("Preprocessing pipeline completed successfully.")
        
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")

if __name__ == "__main__":
    run_pipeline()
