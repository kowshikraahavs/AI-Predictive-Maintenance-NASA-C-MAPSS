import pandas as pd
import numpy as np
from src.utils.logging_utils import get_logger

logger = get_logger(__name__)

def add_rolling_features(df: pd.DataFrame, feature_cols: list, window: int = 5) -> pd.DataFrame:
    """
    Adds rolling mean and standard deviation features for each engine.
    """
    logger.info(f"Adding rolling features with window size {window}...")
    df_out = df.copy()
    
    # Calculate rolling features per unit
    for col in feature_cols:
        df_out[f"{col}_roll_mean"] = df_out.groupby('unit_id')[col].rolling(window=window, min_periods=1).mean().reset_index(level=0, drop=True)
        df_out[f"{col}_roll_std"] = df_out.groupby('unit_id')[col].rolling(window=window, min_periods=1).std().reset_index(level=0, drop=True)
        
        # Fill NaN for std where min_periods=1 didn't have enough data (first row)
        df_out[f"{col}_roll_std"].fillna(0, inplace=True)
        
    return df_out

def generate_sequences(df: pd.DataFrame, sequence_length: int, feature_cols: list) -> tuple:
    """
    Generates time-series sequences for LSTM.
    For each unit, it takes a sliding window of `sequence_length`.
    
    Returns:
        X (np.ndarray): Shape (num_sequences, sequence_length, num_features)
        y (np.ndarray): Shape (num_sequences, )
    """
    logger.info(f"Generating sequences of length {sequence_length}...")
    
    # Check if 'RUL' column exists
    has_rul = 'RUL' in df.columns
    
    seq_gen = (list(gen(df[df['unit_id'] == unit_id], sequence_length, feature_cols, has_rul)) 
               for unit_id in df['unit_id'].unique())
    
    seq_list = list(seq_gen)
    
    # Flatten the list of lists
    if not seq_list or not seq_list[0]:
        return np.array([]), np.array([])
        
    if has_rul:
        seq_array, rul_array = zip(*[item for sublist in seq_list for item in sublist])
        return np.array(seq_array), np.array(rul_array)
    else:
        seq_array = [item for sublist in seq_list for item in sublist]
        return np.array(seq_array), None

def gen(df, seq_length, feature_cols, has_rul):
    """
    Generator function to yield sequences for a single unit.
    """
    data = df[feature_cols].values
    num_elements = data.shape[0]
    
    # We can only generate sequences if we have at least seq_length elements
    if num_elements < seq_length:
        # For test data, if an engine has fewer cycles than sequence_length,
        # we pad it with zeros at the beginning
        pad_size = seq_length - num_elements
        data = np.pad(data, ((pad_size, 0), (0, 0)), 'constant', constant_values=0)
        num_elements = data.shape[0]
        
    for start, stop in zip(range(0, num_elements - seq_length + 1), range(seq_length, num_elements + 1)):
        if has_rul:
            # RUL at the end of the sequence
            yield data[start:stop, :], df['RUL'].iloc[stop - 1]
        else:
            yield data[start:stop, :]

def get_last_sequence_per_unit(df: pd.DataFrame, sequence_length: int, feature_cols: list) -> tuple:
    """
    For test data, we typically only need the LAST sequence of each engine to predict the final RUL.
    """
    logger.info(f"Extracting last sequence of length {sequence_length} for each unit...")
    
    has_rul = 'RUL' in df.columns
    X_last = []
    y_last = []
    
    for unit_id in df['unit_id'].unique():
        unit_data = df[df['unit_id'] == unit_id]
        data = unit_data[feature_cols].values
        num_elements = data.shape[0]
        
        if num_elements < sequence_length:
            # Pad if shorter than sequence
            pad_size = sequence_length - num_elements
            data = np.pad(data, ((pad_size, 0), (0, 0)), 'constant', constant_values=0)
            
        last_seq = data[-sequence_length:, :]
        X_last.append(last_seq)
        
        if has_rul:
            y_last.append(unit_data['RUL'].iloc[-1])
            
    if has_rul:
        return np.array(X_last), np.array(y_last)
    else:
        return np.array(X_last), None
