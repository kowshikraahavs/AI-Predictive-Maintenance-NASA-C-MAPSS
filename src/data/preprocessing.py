import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib
import os
from src.utils.config import MODELS_DIR
from src.utils.logging_utils import get_logger

logger = get_logger(__name__)

def generate_train_rul(train_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the Remaining Useful Life (RUL) for the training data.
    RUL = Max Cycle for the engine - Current Cycle
    """
    logger.info("Generating RUL for training data...")
    # Find the maximum cycle for each unit
    max_cycles = train_df.groupby('unit_id')['cycle'].max().reset_index()
    max_cycles.columns = ['unit_id', 'max_cycle']
    
    # Merge back to the original dataframe
    train_df = pd.merge(train_df, max_cycles, on='unit_id', how='left')
    
    # Calculate RUL
    train_df['RUL'] = train_df['max_cycle'] - train_df['cycle']
    
    # Drop the temporary 'max_cycle' column
    train_df.drop('max_cycle', axis=1, inplace=True)
    
    return train_df

def generate_test_rul(test_df: pd.DataFrame, rul_df: pd.DataFrame) -> pd.DataFrame:
    """
    Assigns the RUL to the test data. The test data only goes up to a certain point.
    The rul_df contains the true RUL for the LAST cycle of each unit.
    We can calculate the max cycle using the true RUL + current last cycle.
    """
    logger.info("Generating true RUL for test data...")
    
    # RUL file has one column with the remaining cycles for each engine's last record
    rul_df = rul_df.copy()
    rul_df['unit_id'] = range(1, len(rul_df) + 1)
    rul_df.rename(columns={'RUL': 'true_rul'}, inplace=True)
    
    # Find the maximum cycle currently in the test set for each unit
    max_cycles = test_df.groupby('unit_id')['cycle'].max().reset_index()
    max_cycles.columns = ['unit_id', 'max_test_cycle']
    
    # Combine max_test_cycle and true_rul to find the absolute max cycle
    max_cycles = pd.merge(max_cycles, rul_df, on='unit_id')
    max_cycles['max_cycle'] = max_cycles['max_test_cycle'] + max_cycles['true_rul']
    
    # Merge absolute max cycle back to test_df
    test_df = pd.merge(test_df, max_cycles[['unit_id', 'max_cycle']], on='unit_id', how='left')
    
    # Calculate RUL for all rows in test_df
    test_df['RUL'] = test_df['max_cycle'] - test_df['cycle']
    
    # Drop temporary column
    test_df.drop('max_cycle', axis=1, inplace=True)
    
    return test_df

def scale_features(train_df: pd.DataFrame, test_df: pd.DataFrame, feature_cols: list) -> tuple:
    """
    Scales the numeric features using StandardScaler.
    IMPORTANT: Fits the scaler ONLY on the training data to prevent data leakage.
    Saves the scaler to disk for later inference.
    """
    logger.info(f"Scaling {len(feature_cols)} features...")
    
    scaler = StandardScaler()
    
    # Fit and transform on training data
    train_scaled = train_df.copy()
    train_scaled[feature_cols] = scaler.fit_transform(train_df[feature_cols])
    
    # Transform test data using the fitted scaler
    test_scaled = test_df.copy()
    test_scaled[feature_cols] = scaler.transform(test_df[feature_cols])
    
    # Save the scaler
    scaler_path = os.path.join(MODELS_DIR, "scaler.joblib")
    joblib.dump(scaler, scaler_path)
    logger.info(f"Scaler saved to {scaler_path}")
    
    return train_scaled, test_scaled, scaler
