import logging

def setup_logger():
    """
    Setup the logger to log to file and console.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Create handlers
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler('bot.log')

    # Create formatter and add it to handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
