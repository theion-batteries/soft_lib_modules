import inspect
import sys
from typing import Dict

from .components import ModuleComponent
from .module import Module


class ModuleFactory:
    """Factory class to create different module"""

    def __init__(self):
        self._module_type: Dict[str, Module] = {}
        self.register_module()

    def __str__(self):
        pass

    def register_module(self):
        """This method dynamically register different module to the dictionary"""
        current_module = sys.modules["src.module"]
        module_name = "Module"
        for name, obj in inspect.getmembers(current_module):
            is_obj = inspect.isclass(obj)
            is_module_name = module_name in name

            if is_obj and is_module_name:
                first_index = name.index(module_name)
                last_index = first_index + len(module_name)
                if (
                    last_index == len(name) and name != module_name
                ):  # register modules to the factory
                    self._module_type[name] = obj

    def get_module(self, module_component: ModuleComponent) -> Module:
        """create the Module instance using ModuleFactory

        Parameters
        -----------
        module_component: ModuleComponent

        Returns
        -------
        Module

        """

        module_type = module_component.module_type
        module = self._module_type.get(module_type)
        if not module:
            raise ValueError(module_type)
        return module(module_component)
