import os

import yaml

from src.module.builder.network_param_builder import build_network_param
from src.util import logger

from conftest import test_dir

def test_network_builder():
    logger.info(test_dir)

    file_name = os.path.join(test_dir,"grbl_module.yaml")
    with open(file_name, "r") as f:
        sys_yaml: yaml.YAMLObject = yaml.safe_load(f)
        network_yaml: yaml.YAMLObject = sys_yaml["cnt_motion"]["network"]
        build_network_param(network_yaml)
