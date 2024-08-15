import logging
import os
from datetime import datetime

def setup_logging(log_dir='logs'):
    """
    Set up logging configuration.
    
    Args:
    log_dir (str): Directory to store log files. Defaults to 'logs'.
    """
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"helicorder_plotter_{timestamp}.log")

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    logging.info(f"Logging initialized. Log file: {log_file}")

def time_function(func):
    """
    A decorator to measure and log the execution time of a function.
    
    Args:
    func (callable): The function to be timed.
    
    Returns:
    callable: The wrapped function.
    """
    import time
    
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logging.info(f"Function {func.__name__} took {end_time - start_time:.2f} seconds to execute.")
        return result
    return wrapper

def validate_config(config):
    """
    Validate the configuration dictionary.
    
    Args:
    config (dict): The configuration dictionary to validate.
    
    Raises:
    ValueError: If the configuration is invalid.
    """
    required_keys = ['network', 'station', 'stream', 'location']
    for station, station_config in config.items():
        for key in required_keys:
            if key not in station_config:
                raise ValueError(f"Missing required key '{key}' for station {station}")
    logging.info("Configuration validated successfully.")
