import logging

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
    
    return logger

def console_handler(level=logging.INFO) -> logging.StreamHandler:
    """Create a console handler with the specified logging level."""
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    return console_handler

