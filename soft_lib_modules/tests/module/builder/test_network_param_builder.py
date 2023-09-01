import os

import yaml

from soft_lib_modules.definitions import CONFIG_DIR
from soft_lib_modules.src.module.builder.network_param_builder import build_network_param


def test_network_builder():
    file_name = os.path.join(CONFIG_DIR, "grbl_module.yaml")
    with open(file_name, "r") as f:
        sys_yaml: yaml.YAMLObject = yaml.safe_load(f)
        network_yaml: yaml.YAMLObject = sys_yaml["cnt_motion"]["network"]
        build_network_param(network_yaml)
