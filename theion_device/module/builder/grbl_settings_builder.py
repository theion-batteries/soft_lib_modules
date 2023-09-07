import yaml

from .grbl_configuration import grbl_config


def build_grbl_settings(file_name: str):
    try:
        grbl_settings_yaml: yaml.YAMLObject = None
        with open(file_name, "r") as f:
            grbl_settings_yaml = yaml.safe_load(f)
            settings = grbl_settings_yaml.get("settings")
            settings_list = {}
            for key, value in grbl_config.items():
                settings_list[value] = settings[key]
                # settings_list.append("{}={}".format(value,settings[key]))
            return settings_list
    except Exception as e:
        pass
