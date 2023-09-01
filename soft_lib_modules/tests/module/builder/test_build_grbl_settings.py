import os

from soft_lib_modules.definitions import CONFIG_DIR, logger
from soft_lib_modules.src.module.builder.grbl_settings_builder import build_grbl_settings


def test_build_grbl_settings():
    result = build_grbl_settings("cnt_motion")
    for r in result:
        logger.trace(r)

