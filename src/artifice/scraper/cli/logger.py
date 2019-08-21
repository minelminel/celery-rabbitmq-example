import sys
import logging

def configure_logger(configuration):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handlers = []

    if configuration.LOG_FILE is not None:
        file_handler = logging.FileHandler(filename=configuration.LOG_FILE, mode='a')
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)
    if configuration.STDOUT is True:
        stream_handler = logging.StreamHandler(stream=sys.stdout)
        stream_handler.setFormatter(formatter)
        handlers.append(stream_handler)

    logging.basicConfig(
        datefmt='%m/%d/%Y %I:%M:%S %p',
        level=getattr(logging, configuration.LOG_LEVEL),
        handlers=handlers
    )
