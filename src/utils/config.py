import os
from pathlib import Path

# Base Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MODELS_DIR = PROJECT_ROOT / "models" / "saved"
REPORTS_DIR = PROJECT_ROOT / "reports" / "figures"

# Ensure directories exist
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

# Dataset Files
TRAIN_FILE = RAW_DATA_DIR / "train_FD001.txt"
TEST_FILE = RAW_DATA_DIR / "test_FD001.txt"
RUL_FILE = RAW_DATA_DIR / "RUL_FD001.txt"

# Columns Definition
INDEX_COLUMNS = ["unit_id", "cycle"]
SETTING_COLUMNS = ["op_setting_1", "op_setting_2", "op_setting_3"]
SENSOR_COLUMNS = [f"sensor_{i}" for i in range(1, 22)]
ALL_COLUMNS = INDEX_COLUMNS + SETTING_COLUMNS + SENSOR_COLUMNS

# Modeling Parameters
SEQUENCE_LENGTH = 30
TEST_SIZE = 0.2
RANDOM_STATE = 42

# LSTM Parameters
BATCH_SIZE = 64
EPOCHS = 50
LEARNING_RATE = 0.001
FAST_MODE = False  # Set to True for quicker training during development

# Health Status Thresholds
HEALTHY_THRESHOLD = 50
WARNING_THRESHOLD = 20
