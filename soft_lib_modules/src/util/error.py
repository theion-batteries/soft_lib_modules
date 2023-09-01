from .log import LOG_CONFIG_ERROR, Log


class _LoggedError(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)
        # Log.get_instance().enable(LOG_CONFIG_ERROR)
        Log.get_instance().error(msg)


class KeyenceException(_LoggedError):
    pass


class StreamConnectionLostException(Exception):
    def __init__(self, message):
        pass


class InvalidPositionError(_LoggedError):
    """
    Sometimes microcontroller send position value which is not unicode
    """

    pass


class ExecuteStepError(_LoggedError):
    """
    Error retlated to executing the status
    """

    pass


class WGMBuildProcessError(_LoggedError):
    """
    Error retated to building the ProcessComponent
    """

    pass


class WGMBuildModuleError(_LoggedError):
    """
    Error retated to building the System
    """

    pass


class WGMBuildCommandError(_LoggedError):
    """
    Error retated to building the Command
    """

    pass


class WGMBuildConfigParameterError(_LoggedError):
    """
    Error retated to building the Configuration Parameter
    """

    pass


class WGMBuildNetworkParameterError(_LoggedError):
    """
    Error retated to building the Network Parameter
    """

    pass


class TCPClientException(_LoggedError):
    """
    Error related to TCP Connection
    """

    pass


class KeyenceException(_LoggedError):
    """
    Error related to Keyence
    """

    pass
