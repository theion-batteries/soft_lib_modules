import os
from pathlib import Path

from theion_device.util import LOG_CONFIG_TRACE_CONSOLE_ONLY, Log

root_dir = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir))


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root


CONFIG_DIR = os.path.join(ROOT_DIR, "config")


SETTINGS_DIR = os.path.join(CONFIG_DIR, "settings")

STEP_DIR = os.path.join(ROOT_DIR, "instructions")


LOG_CONFIG_MODE = LOG_CONFIG_TRACE_CONSOLE_ONLY


@staticmethod
def get_logger():
    logger = Log.get_instance()

    logger.enable(LOG_CONFIG_MODE)
    return logger


logger = get_logger()
