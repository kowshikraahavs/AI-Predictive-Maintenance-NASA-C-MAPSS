import os
import pandas as pd
import numpy as np
from src.utils.config import TRAIN_FILE, TEST_FILE, RUL_FILE, ALL_COLUMNS
from src.utils.logging_utils import get_logger

logger = get_logger(__name__)

class DataValidationError(Exception):
    """Custom exception for data validation errors."""
    pass

def validate_files_exist():
    """Checks if the required dataset files exist."""
    required_files = [
        (TRAIN_FILE, "Training Data"),
        (TEST_FILE, "Testing Data"),
        (RUL_FILE, "RUL Data")
    ]
    
    missing_files = []
    for filepath, name in required_files:
        if not os.path.exists(filepath):
            missing_files.append(f"{name} ({filepath})")
            
    if missing_files:
        error_msg = f"Missing required dataset files: {', '.join(missing_files)}. Please download the C-MAPSS FD001 dataset and place it in the data/raw/ directory."
        logger.error(error_msg)
        raise DataValidationError(error_msg)
    
    logger.info("All required dataset files are present.")
    return True

def validate_dataframe(df: pd.DataFrame, is_rul: bool = False, test_units: int = None):
    """
    Validates a loaded DataFrame for expected structure and content.
    """
    if is_rul:
        # RUL file should just have one column (or we treat it as 1 column)
        if len(df.columns) != 1:
            raise DataValidationError(f"RUL dataset should have exactly 1 column, but has {len(df.columns)}.")
        
        if df.isnull().values.any():
            raise DataValidationError("RUL dataset contains missing values.")
            
        if not pd.api.types.is_numeric_dtype(df.iloc[:, 0]):
            raise DataValidationError("RUL values must be numeric.")
            
        if test_units is not None and len(df) != test_units:
            raise DataValidationError(f"RUL dataset length ({len(df)}) does not match the number of unique units in the test set ({test_units}).")
        
        return True

    # Validate main dataset (Train/Test)
    if len(df.columns) != len(ALL_COLUMNS):
        raise DataValidationError(f"Expected {len(ALL_COLUMNS)} columns, but got {len(df.columns)}.")
        
    if df.isnull().values.any():
        raise DataValidationError("Dataset contains unexpected missing values.")
        
    if not pd.api.types.is_numeric_dtype(df["unit_id"]) or not pd.api.types.is_numeric_dtype(df["cycle"]):
        raise DataValidationError("Unit IDs and Cycles must be numeric.")
        
    if (df["unit_id"] <= 0).any() or (df["cycle"] <= 0).any():
        raise DataValidationError("Unit IDs and Cycles must be strictly positive.")
        
    # Check if sensor values are numeric
    sensor_cols = [col for col in df.columns if "sensor" in col or "op_setting" in col]
    for col in sensor_cols:
        if not pd.api.types.is_numeric_dtype(df[col]):
            raise DataValidationError(f"Column {col} contains non-numeric values.")

    return True

def validate_all_data(train_df: pd.DataFrame, test_df: pd.DataFrame, rul_df: pd.DataFrame):
    """
    Runs all validation checks on the loaded dataframes.
    """
    logger.info("Starting data validation...")
    
    validate_dataframe(train_df)
    logger.info("Training data format validated.")
    
    validate_dataframe(test_df)
    logger.info("Testing data format validated.")
    
    num_test_units = test_df['unit_id'].nunique()
    validate_dataframe(rul_df, is_rul=True, test_units=num_test_units)
    logger.info("RUL data format and dimensions validated.")
    
    logger.info("Data validation completed successfully.")
    return True
