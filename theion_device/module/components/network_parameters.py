from dataclasses import dataclass


@dataclass
class NetworkParam:
    """Dataclass containing the list of Parameters required for the connection to controller

    Attributes
    -----------
    ip : str
        ip address of the module

    port: int
        port of the module

    timeout: int
        timeout required for the connection timeout

    buffer_size: int
        size of the buffer

    """

    ip: str
    port: int
    timeout: int
    buffer_size: int
