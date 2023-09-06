import os

from src.util import logger
from src.module.grbl_module.grbl_settings_parser import GrblSettingsParser

from conftest import settings_dir

def test_grbl_settings_parser():
    setting_file_name = os.path.join(settings_dir,"cnt_motion.yaml")
    motion = GrblSettingsParser(setting_file_name)
    logger.info(motion.grbl_settings())

