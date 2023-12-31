import os
from typing import Optional

import yaml

from theion_device.util import logger

from ..communication import (Client, KeyenceClient, MeteorClient,
                             TCPStreamClient)
from ..components import ModuleComponent, NetworkParam
from .network_param_builder import build_network_param


def CreateClient(module_type: str, network_param: NetworkParam) -> Client:
    """This function create the client required to manage conenction to the module

    Parameters
    ----------
    module_type: str
        type of the module

    network_param: NetworkParam
        network parameters

    Returns
    --------
    Client

    """

    client: Optional[Client] = None
    if module_type == "KeyenceModule":
        client = KeyenceClient(
            network_param.ip, network_param.port, network_param.buffer_size
        )

    elif module_type == "MeteorModule":
        client = MeteorClient(
            network_param.ip, network_param.port, network_param.buffer_size
        )

    else:
        client = TCPStreamClient(
            network_param.ip, network_param.port, network_param.buffer_size
        )
    return client


def build_module_component(
    yaml_file: str = "", module_name: str = ""
) -> ModuleComponent:
    """build module components.It takes either yaml_name and file_name to build yaml object or yaml object

    Parameters
    -----------
    yaml_file: str
        - name of the YAML file which contains related components of the Module

    module_name: str
        - assigned name to the particular module



    Returns
    --------
    ModuleComponent

    """
    try:
        module_yaml: yaml.YAMLObject = load_yaml(yaml_file)
        commands: yaml.YAMLObject = module_yaml.get("commands")
        module_type: str = module_yaml.get("module_type")
        network_params: NetworkParam = build_network_param(
            module_yaml.get(module_name).get("network")
        )
        client: Client = CreateClient(module_type, network_params)
        logger.trace("ModuleComponent name: {}".format(module_name))
        module_component: ModuleComponent = ModuleComponent(
            module_name,
            module_type,
            commands,
            network_params,
            client,
        )
        return module_component
    except Exception as e:
        raise e


def load_yaml(yaml_file: str) -> ModuleComponent:
    try:
        logger.trace(yaml_file)
        module_yaml: yaml.YAMLObject = None
        with open(yaml_file, "r") as f:
            module_yaml = yaml.safe_load(f)

    except Exception as e:
        raise e
    return module_yaml
