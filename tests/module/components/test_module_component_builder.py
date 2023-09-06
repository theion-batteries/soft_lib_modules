import os

from src.module.builder.module_component_builder import build_module_component


def test_build_module_component():
    file = "grbl_module.yaml"
    result = build_module_component("grbl_module", "cnt_motion")
    assert result
    pass
