import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd
from src.utils.config import REPORTS_DIR

def plot_actual_vs_predicted(y_true, y_pred, model_name):
    plt.figure(figsize=(10, 6))
    plt.scatter(y_true, y_pred, alpha=0.5, color='blue')
    
    # Plot perfect prediction line
    max_val = max(max(y_true), max(y_pred))
    plt.plot([0, max_val], [0, max_val], 'r--')
    
    plt.title(f'{model_name} - Actual vs Predicted RUL')
    plt.xlabel('Actual RUL')
    plt.ylabel('Predicted RUL')
    plt.grid(True, alpha=0.3)
    
    filename = f"{model_name.replace(' ', '_').lower()}_actual_vs_predicted.png"
    plt.savefig(os.path.join(REPORTS_DIR, filename), bbox_inches='tight')
    plt.close()

def plot_model_comparison(metrics_dict):
    df = pd.DataFrame(metrics_dict).T
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # Plot MAE
    sns.barplot(x=df.index, y=df['MAE'], ax=axes[0], palette='viridis')
    axes[0].set_title('Mean Absolute Error (Lower is Better)')
    axes[0].set_ylabel('MAE')
    
    # Plot RMSE
    sns.barplot(x=df.index, y=df['RMSE'], ax=axes[1], palette='viridis')
    axes[1].set_title('Root Mean Squared Error (Lower is Better)')
    axes[1].set_ylabel('RMSE')
    
    # Plot R2
    sns.barplot(x=df.index, y=df['R2'], ax=axes[2], palette='viridis')
    axes[2].set_title('R-Squared (Higher is Better)')
    axes[2].set_ylabel('R2 Score')
    
    for ax in axes:
        ax.tick_params(axis='x', rotation=45)
        
    plt.tight_layout()
    plt.savefig(os.path.join(REPORTS_DIR, 'model_comparison.png'), bbox_inches='tight')
    plt.close()

def plot_engine_degradation(cycles, actual_rul, predicted_rul=None, engine_id=None):
    plt.figure(figsize=(12, 6))
    plt.plot(cycles, actual_rul, label='Actual RUL', color='green', linewidth=2)
    
    if predicted_rul is not None:
        plt.plot(cycles, predicted_rul, label='Predicted RUL', color='red', linestyle='--')
        
    title = 'Engine Degradation Curve'
    if engine_id is not None:
        title += f' (Unit {engine_id})'
        
    plt.title(title)
    plt.xlabel('Operating Cycle')
    plt.ylabel('Remaining Useful Life (RUL)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    filename = f"engine_{engine_id}_degradation.png" if engine_id else "engine_degradation.png"
    plt.savefig(os.path.join(REPORTS_DIR, filename), bbox_inches='tight')
    plt.close()
