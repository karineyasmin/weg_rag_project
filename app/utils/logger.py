import logging
import sys


def setup_custom_logger(name: str) -> logging.Logger:
    """
    Configures a standard logger for the application.

    Args:
        name (str): The name of the module generating the logs.

    Returns:
        logging.Logger: A configured logger instance.
    """

    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger
