from os import path

import pytest
import yaml

from conftest import config_dir
from src.module.builder.module_component_builder import build_module_component
from src.util import logger


@pytest.mark.parametrize(
    "module_type,module_name",
    [
        ("keyence", "whs_keyence"),
        ("dispenser", "cnt_dispenser"),
        ("trigger", "ph_trigger"),
        ("high_voltage", "minipuls"),
        ("grbl_module", "cnt_motion"),
        ("grbl_module", "ph_motion"),
        ("grbl_module", "whs_motion"),
    ],
)
def test_module_compone_builder_builder(module_type, module_name):
    test_dir = path.join(config_dir, "test")
    file_name = path.join(test_dir, module_type + ".yaml")

    with open(file_name, "r") as f:
        module_yaml: yaml.YAMLObject = yaml.safe_load(f)
        module = build_module_component(file_name, module_name)
        assert module_yaml["commands"] == module.commands
