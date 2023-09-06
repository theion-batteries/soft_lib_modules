import os

from src.module.builder.module_component_builder import build_module_component
from conftest import test_dir

def test_build_module_component():
    file = os.path.join(test_dir,"grbl_module.yaml")
    result = build_module_component(file, "cnt_motion")
    assert result
    pass
