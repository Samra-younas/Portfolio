"""
Logging utilities for the chatbot application.
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from config.settings import get_config

def setup_logger(name: str = None) -> logging.Logger:
    """
    Set up logging configuration.
    
    Args:
        name: Logger name (defaults to app logger)
        
    Returns:
        logging.Logger: Configured logger
    """
    config = get_config()
    
    # Create logger
    logger = logging.getLogger(name or __name__)
    logger.setLevel(getattr(logging, config.LOG_LEVEL))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler with rotation
    if config.LOG_FILE:
        # Ensure logs directory exists
        os.makedirs(os.path.dirname(config.LOG_FILE), exist_ok=True)
        
        file_handler = RotatingFileHandler(
            config.LOG_FILE,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(getattr(logging, config.LOG_LEVEL))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def get_logger(name: str = None) -> logging.Logger:
    """
    Get a logger instance.
    
    Args:
        name: Logger name
        
    Returns:
        logging.Logger: Logger instance
    """
    return logging.getLogger(name or __name__)
