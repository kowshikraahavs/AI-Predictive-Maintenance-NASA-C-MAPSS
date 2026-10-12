import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.utils.config import RAW_DATA_DIR, REPORTS_DIR, ALL_COLUMNS
from src.utils.logging_utils import get_logger

logger = get_logger(__name__)

def run_eda():
    logger.info("Starting Exploratory Data Analysis (EDA)...")
    os.makedirs(os.path.join(REPORTS_DIR, 'figures'), exist_ok=True)
    
    # Load raw training data
    train_path = os.path.join(RAW_DATA_DIR, "train_FD001.txt")
    df = pd.read_csv(train_path, sep=r'\s+', header=None)
    
    # Handle potentially extra columns caused by trailing spaces
    if df.shape[1] > len(ALL_COLUMNS):
        df = df.iloc[:, :len(ALL_COLUMNS)]
    df.columns = ALL_COLUMNS
    
    # 1. Engine Lifespan Distribution
    logger.info("Generating Engine Lifespan Distribution...")
    lifespans = df.groupby('unit_id')['cycle'].max()
    plt.figure(figsize=(10, 6))
    sns.histplot(lifespans, bins=20, kde=True, color='#4A90E2')
    plt.title('Distribution of Engine Lifespans (Max Cycles)')
    plt.xlabel('Max Cycles (Failure Point)')
    plt.ylabel('Count of Engines')
    plt.savefig(os.path.join(REPORTS_DIR, 'figures', 'engine_lifespan_distribution.png'))
    plt.close()
    
    # 2. Sensor Trend Example (Engine 1)
    logger.info("Generating Sensor Trend Plot for Engine 1...")
    engine_1 = df[df['unit_id'] == 1]
    sensors_to_plot = ['sensor_2', 'sensor_3', 'sensor_4', 'sensor_7']
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Sensor Degradation Trends for Engine 1', fontsize=16)
    
    for i, sensor in enumerate(sensors_to_plot):
        ax = axes[i//2, i%2]
        ax.plot(engine_1['cycle'], engine_1[sensor], color='#e74c3c')
        ax.set_title(f'{sensor} over time')
        ax.set_xlabel('Cycle')
        ax.set_ylabel('Sensor Value')
        
    plt.tight_layout()
    plt.savefig(os.path.join(REPORTS_DIR, 'figures', 'engine_1_sensor_trends.png'))
    plt.close()
    
    # 3. Correlation Heatmap
    logger.info("Generating Correlation Heatmap...")
    # Drop unit_id and cycle for correlation, as well as constant sensors
    constant_sensors = ['op_setting_3', 'sensor_1', 'sensor_5', 'sensor_10', 'sensor_16', 'sensor_18', 'sensor_19']
    cols_to_drop = ['unit_id', 'cycle'] + constant_sensors
    corr_df = df.drop(columns=[c for c in cols_to_drop if c in df.columns])
    
    plt.figure(figsize=(16, 12))
    corr_matrix = corr_df.corr()
    sns.heatmap(corr_matrix, annot=False, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Sensor Correlation Heatmap')
    plt.tight_layout()
    plt.savefig(os.path.join(REPORTS_DIR, 'figures', 'correlation_heatmap.png'))
    plt.close()
    
    logger.info("EDA successfully completed. Figures saved to reports/figures/")

if __name__ == "__main__":
    run_eda()
