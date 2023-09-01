import os

import pytest
import yaml

from soft_lib_modules.definitions import CONFIG_DIR, logger
from soft_lib_modules.src.module.builder.module_component_builder import build_module_component


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
def test_keyence_builder(module_type, module_name):
    file_name = os.path.join(CONFIG_DIR, module_type + ".yaml")

    with open(file_name, "r") as f:
        module_yaml: yaml.YAMLObject = yaml.safe_load(f)
        module = build_module_component(module_type, module_name)
        assert module_yaml["commands"] == module.commands
