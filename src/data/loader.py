import pandas as pd
from src.utils.config import TRAIN_FILE, TEST_FILE, RUL_FILE, ALL_COLUMNS
from src.utils.logging_utils import get_logger
from src.data.validation import validate_files_exist, validate_all_data

logger = get_logger(__name__)

def load_data():
    """
    Loads the training, testing, and RUL datasets.
    Performs initial file existence check and full dataset validation.
    
    Returns:
        tuple: (train_df, test_df, rul_df)
    """
    logger.info("Initiating dataset loading process...")
    
    # 1. Check if files exist
    validate_files_exist()
    
    try:
        # Load training data
        # The dataset is space separated. We drop the last two NaN columns if they appear due to trailing spaces.
        train_df = pd.read_csv(TRAIN_FILE, sep=r'\s+', header=None)
        if train_df.shape[1] > len(ALL_COLUMNS):
            train_df = train_df.iloc[:, :len(ALL_COLUMNS)]
        train_df.columns = ALL_COLUMNS
        
        # Load testing data
        test_df = pd.read_csv(TEST_FILE, sep=r'\s+', header=None)
        if test_df.shape[1] > len(ALL_COLUMNS):
            test_df = test_df.iloc[:, :len(ALL_COLUMNS)]
        test_df.columns = ALL_COLUMNS
        
        # Load RUL data
        rul_df = pd.read_csv(RUL_FILE, sep=r'\s+', header=None)
        rul_df.columns = ['RUL']
        
        logger.info(f"Loaded Train shape: {train_df.shape}, Test shape: {test_df.shape}, RUL shape: {rul_df.shape}")
        
        # 2. Validate loaded dataframes
        validate_all_data(train_df, test_df, rul_df)
        
        return train_df, test_df, rul_df
        
    except Exception as e:
        logger.error(f"Failed to load and validate datasets: {str(e)}")
        raise
