import logging
import sys

def get_logger(name: str) -> logging.Logger:
    """
    Creates and configures a logger.
    """
    logger = logging.getLogger(name)
    
    # Avoid adding multiple handlers if logger already exists
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Create console handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Add formatter to ch
        ch.setFormatter(formatter)
        
        # Add ch to logger
        logger.addHandler(ch)
        
    return logger
