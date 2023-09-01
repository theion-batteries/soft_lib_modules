import pytest

from soft_lib_modules.definitions import logger
from soft_lib_modules.src.module.grbl_module.grbl_settings_parser import GrblSettingsParser


def test_grbl_settings_parser():
    motion = GrblSettingsParser("cnt_motion")
    logger.info(motion.grbl_settings())

