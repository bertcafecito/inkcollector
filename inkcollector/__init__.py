import configparser
import logging
import os
from importlib.metadata import version, PackageNotFoundError

from inkcollector.utils.log import setup_logger
from inkcollector.utils.output import friendly_filepath, output_json, output_csv

try:
    __version__ = version("inkcollector")
except PackageNotFoundError:
    __version__ = "unknown"

class InkCollector:
    def __init__(self, name="inkcollector", config_file="config.ini"):
        self.version = __version__
        self.name = name
        self.description = "Inkcollector is a CLI tool for collecting data about the disney lorcana trading card game."
        self.config_file = config_file
        self.config = self.load_config()

    @property
    def logger(self):
        """
        Returns a logger instance for the InkCollector class.
        
        The logger is configured with the name of the class and the specified logging level.
        
        Returns:
            logging.Logger: Configured logger instance.
        """
        return setup_logger()
    
    def log(self, message: str, level: int = logging.INFO):
        """
        Logs a message with the specified logging level.
        
        Args:
            message (str): The message to log.
            level (int): The logging level. Default is logging.INFO.
        """
        self.logger.log(level, message)

    def load_config(self):
        """
        Loads the configuration from the config file.
        
        Returns:
            configparser.ConfigParser: The loaded configuration.
        """
        config = configparser.ConfigParser()
        if os.path.exists(self.config_file):
            config.read(self.config_file)
            self.log(f"Loaded configuration from {self.config_file}.", logging.INFO)
        else:
            self.log(f"Configuration file {self.config_file} not found. Using default settings.", logging.WARNING)
        return config

    def file_output(self, data, filepath):
        """
        Save data to a file.
        
        Args:
            data (str): The data to save.
            filepath (str): The path to the file where the data will be saved.
        """
        data_dir = self.config.get("Directories", "Data", fallback="data")

        # Make the filepath friendly for the file system
        filepath = friendly_filepath(filepath)

        # Join the data directory with the provided filepath
        filepath = os.path.join(data_dir, filepath)

        # Check if the filepath contains subdirectories
        if os.path.dirname(filepath):
            # Create the directories if they do not exist
            if not os.path.exists(os.path.dirname(filepath)):
                os.makedirs(os.path.dirname(filepath))
                self.log("Created directories for the file path.", logging.INFO)

        # Get the file extension from the filepath
        file_extension = os.path.splitext(filepath)[1].lower()
        supported_formats = ['.json', '.csv']
        if file_extension not in supported_formats:
            self.log(f"Unsupported file format: {file_extension}. Supported formats are: {supported_formats}", logging.ERROR)
            return None
        
        if file_extension == '.json':
            output_json(data, filepath)
            self.log("Saved data to JSON file.", logging.INFO)
            return True

        if file_extension == '.csv':
            output_csv(data, filepath)
            self.log("Saved data to CSV file.", logging.INFO)
            return True
        
        self.log("Unsupported file format. Supported formats are: .json, .csv", logging.ERROR)
        return None

        