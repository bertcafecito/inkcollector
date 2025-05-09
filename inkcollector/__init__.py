import logging
from importlib.metadata import version, PackageNotFoundError

from inkcollector.utils.log import setup_logger

try:
    __version__ = version("inkcollector")
except PackageNotFoundError:
    __version__ = "unknown"

class InkCollector:
    def __init__(self, name="inkcollector"):
        self.version = __version__
        self.name = name
        self.description = "Inkcollector is a CLI tool for collecting data about the disney lorcana trading card game."
        
    @property
    def logger(self):
        """
        Returns a logger instance for the InkCollector class.
        
        The logger is configured with the name of the class and the specified logging level.
        
        Returns:
            logging.Logger: Configured logger instance.
        """
        return setup_logger(self.name)
    
    def log(self, message: str, level: int = logging.INFO):
        """
        Logs a message with the specified logging level.
        
        Args:
            message (str): The message to log.
            level (int): The logging level. Default is logging.INFO.
        """
        self.logger.log(level, message)