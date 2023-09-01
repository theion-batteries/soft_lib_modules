import inspect
import sys
from typing import Dict

import yaml

from definitions import logger
from src.util import WGMBuildModuleError

from ..components import ModuleComponent
from ..dispenser_module import DispenserModule
from ..grbl_module import GrblModule
from ..keyence_module import KeyenceModule
from ..module import Module
from ..module_factory import ModuleFactory
from ..trigger_module import TriggerModule
from .module_component_builder import build_module_component


def build_module(yaml_name: str = "", module_name: str = "") -> Module:
    """Build the module. It takes either yaml_name and module_name to build yaml object or yaml object

    Parameters
    -----------
    yaml_name: str

    module_name: str

    module_yaml: YAMLObject


    Returns
    --------
    Module

    """
    try:
        module_component: ModuleComponent = build_module_component(
            yaml_name=yaml_name, module_name=module_name
        )
        factory = ModuleFactory()

        module: Module = factory.get_module(module_component=module_component)
        return module
    except Exception as e:
        raise WGMBuildModuleError(str(e))
