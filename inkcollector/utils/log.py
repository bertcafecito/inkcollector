import logging
import os
from datetime import datetime, timezone

def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Set up a logger with the specified name and level.

    Args:
        name (str): The name of the logger.
        level (int): The logging level. Default is logging.INFO.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create console handler with a higher log level
    ch = console_handler(level)
    logger.addHandler(ch)

    # Create file handler which logs even debug messages in the logs folder

    # Create logs directory in current directory to store logs
    logs_dir = os.path.join(os.getcwd(), "logs")

    # Create logs directory if it doesn't exist
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    # Add timestamp to the log filename
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    log_filename = f"logs/{name}_{timestamp}.log"

    # Create file handler which logs even debug messages in the logs folder
    fh = file_handler(log_filename, level)
    logger.addHandler(fh)

    return logger

def console_handler(level=logging.INFO) -> logging.StreamHandler:
    """Create a console handler with the specified logging level."""
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    return console_handler

def file_handler(filename: str, level=logging.INFO) -> logging.FileHandler:
    """Create a file handler with the specified logging level."""
    file_handler = logging.FileHandler(filename)
    file_handler.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    return file_handler
