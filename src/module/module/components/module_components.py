from dataclasses import dataclass
from typing import Optional

from yaml import YAMLObject

from ..communication import Client
from .network_parameters import NetworkParam

# from src.communication import Client


@dataclass
class ModuleComponent:
    """Data class containing components  required by Modules

    Attributes
    -----------
    module_name: str
        unique name of the module

    module_type: str
        type of the module - grbl, keyence, dispenser

    module_available: bool
        this is required when the module is used in the process context

    commands : YAMLObject
        list of commands associated to the module

    network_parameter: NetworkParam
        network details like IP address, port, buffersize of the module

    client: Client
        Client manages the connection to the module

    """

    module_name: str
    module_type: str
    commands: YAMLObject
    network_parameters: NetworkParam
    client: Optional[Client] = None
