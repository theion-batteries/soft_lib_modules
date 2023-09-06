from src.util import logger
from src.module.grbl_module.grbl_settings_parser import GrblSettingsParser


def test_grbl_settings_parser():
    motion = GrblSettingsParser("cnt_motion")
    logger.info(motion.grbl_settings())

