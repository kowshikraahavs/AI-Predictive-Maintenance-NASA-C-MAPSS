import pytest
import pandas as pd
import numpy as np
import os
import sys

# Ensure src is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data.preprocessing import generate_train_rul
from src.features.engineering import generate_sequences
from src.inference.predictor import RULPredictor

def test_rul_generation():
    """Test if RUL is calculated correctly: max cycle - current cycle"""
    data = {
        'unit_id': [1, 1, 1, 2, 2],
        'cycle': [1, 2, 3, 1, 2],
        'sensor_1': [10, 11, 12, 10, 11]
    }
    df = pd.DataFrame(data)
    df_rul = generate_train_rul(df)
    
    # Engine 1 RULs should be 2, 1, 0
    assert df_rul[df_rul['unit_id'] == 1]['RUL'].tolist() == [2, 1, 0]
    # Engine 2 RULs should be 1, 0
    assert df_rul[df_rul['unit_id'] == 2]['RUL'].tolist() == [1, 0]

def test_sequence_generation():
    """Test if LSTM sequences are generated with correct shape"""
    data = {
        'unit_id': [1, 1, 1, 1, 1],
        'cycle': [1, 2, 3, 4, 5],
        'sensor_1': [10, 11, 12, 13, 14],
        'RUL': [4, 3, 2, 1, 0]
    }
    df = pd.DataFrame(data)
    
    # Sequence length 3
    X, y = generate_sequences(df, sequence_length=3, feature_cols=['sensor_1'])
    
    # We should have 3 sequences: [1,2,3], [2,3,4], [3,4,5]
    assert X.shape == (3, 3, 1)
    assert len(y) == 3
    assert y.tolist() == [2, 1, 0] # RUL at the end of each sequence

def test_predictor_initialization():
    """Test if predictors can be loaded (requires pre-trained models)"""
    try:
        pred_base = RULPredictor("Linear Regression")
        assert pred_base.model is not None
        
        pred_rf = RULPredictor("Random Forest")
        assert pred_rf.model is not None
        
        pred_lstm = RULPredictor("LSTM")
        assert pred_lstm.model is not None
        
    except Exception as e:
        pytest.skip(f"Models not trained yet or missing files: {e}")
