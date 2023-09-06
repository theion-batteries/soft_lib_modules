import yaml

from src.util import logger

from ..components.network_parameters import NetworkParam


def build_network_param(network_yaml: yaml.YAMLObject) -> NetworkParam:
    """build the network parameter from the yaml object

    Parameters
    -----------
    network_yaml: YAMLObject

    Returns
    -------
    NetworkParam

    """
    network_parameters: NetworkParam = NetworkParam(
        network_yaml["ip"],
        network_yaml["port"],
        network_yaml["timeout"],
        network_yaml["buffer_size"],
    )
    logger.trace(network_parameters)
    return network_parameters
