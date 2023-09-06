import os

from definitions import CONFIG_DIR
from src.module.builder.module_component_builder import build_module_component


def test_build_module_component():
    file = os.path.join(CONFIG_DIR, "grbl_module.yaml")
    result = build_module_component("grbl_module", "cnt_motion")
    assert result
    pass
