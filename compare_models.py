import json
import os
from src.utils.config import MODELS_DIR
from src.evaluation.plots import plot_model_comparison
from src.utils.logging_utils import get_logger

logger = get_logger(__name__)

def run_comparison():
    logger.info("Generating Model Comparison Plots...")
    
    metrics_path = os.path.join(MODELS_DIR, "ml_metrics.json")
    
    if not os.path.exists(metrics_path):
        logger.error(f"Metrics file not found at {metrics_path}")
        return
        
    with open(metrics_path, "r") as f:
        metrics = json.load(f)
        
    plot_model_comparison(metrics)
    
    logger.info("Comparison plots generated in reports/figures/")

if __name__ == "__main__":
    run_comparison()
