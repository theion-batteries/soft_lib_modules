import os

import yaml

from src.util import logger


class GrblSettingsParser:
    def __init__(self, settings_file_name):
        self._module_settings_file = settings_file_name
        self.__load_yaml()

    def __load_yaml(self):
        try:
            module_settings_yaml: yaml.YAMLObject = None
            with open(self._module_settings_file, "r") as f:
                self.__module_settings_yaml = yaml.safe_load(f)

        except Exception as e:
            logger.error(str(e))

    def grbl_settings(self):
        return self.__module_settings_yaml["settings"]
