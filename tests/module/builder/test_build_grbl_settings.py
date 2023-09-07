from os import path

from conftest import settings_dir
from theion_device.module.builder.grbl_settings_builder import build_grbl_settings
from theion_device.util import logger


def test_build_grbl_settings():
    logger.trace(settings_dir)
    yaml_file = path.join(settings_dir, "cnt_motion.yaml")
    result = build_grbl_settings(yaml_file)
    for r in result:
        logger.trace(r)
