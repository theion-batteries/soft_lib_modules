import os

from conftest import test_dir
from src.module.builder.module_component_builder import build_module_component


def test_build_module_component():
    file = os.path.join(test_dir, "grbl_module.yaml")
    result = build_module_component(file, "cnt_motion")
    assert result
    pass
