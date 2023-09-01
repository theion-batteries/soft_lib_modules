import os
from pathlib import Path

from soft_lib_modules.src.util.log import (
    LOG_CONFIG_INFO_CONSOLE_ONLY,
    LOG_CONFIG_TRACE_CONSOLE_ONLY,
    Log,
)


root_dir = os.path.abspath(os.path.join(os.path.abspath(__file__), os.pardir))


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root
ROOT_DIR =  Path(ROOT_DIR).resolve().parents[0]


CONFIG_DIR = os.path.join(ROOT_DIR, "config")


SETTINGS_DIR = os.path.join(CONFIG_DIR, "settings")

STEP_DIR = os.path.join(ROOT_DIR, "instructions")


DLL_DIR = os.path.join(ROOT_DIR, "soft_lib_modules/src/module/communication/src/dll")
KEYENCE_DLL = "keyenceLib.dll"
KEYENCE_DLL_PATH = os.path.join(DLL_DIR, KEYENCE_DLL)

TEST_CONFIG_DIR = os.path.join(ROOT_DIR, "test")

LOG_CONFIG_MODE = LOG_CONFIG_TRACE_CONSOLE_ONLY


@staticmethod
def get_logger():
    logger = Log.get_instance()
    logger.enable(LOG_CONFIG_MODE)
    return logger


logger = get_logger()
