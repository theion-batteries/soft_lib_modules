import time
from abc import ABC

import yaml

from definitions import logger

from .communication import Response, retry
from .components import ModuleComponent


class Module(ABC):
    """Base class for all the Modules. It encapsulate functions required for individual models"""

    def __init__(self, eol: str, ack_str: str, module_component: ModuleComponent):
        """
        Parameters
        ---------
        eof: str
        ack_str: str
        module_component: ModuleComponent

        """
        self._ack_str = ack_str
        self._eol = eol
        self._module_name: str = module_component.module_name
        self._client = module_component.client
        self._commands: yaml.YAMLObject = module_component.commands

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, exc_traceback):
        # result = await self.__aexit__(exc_type, exc_value, exc_traceback)
        logger.info("Module {} {}".format(self._module_name, ""))

        if exc_type is not None:
            logger.info(
                "Module {} exited due to {} : {}".format(
                    self._module_name, exc_type, exc_value
                )
            )

    def get_command(self, value: str):
        return self._commands.get(value, "")

    def _handle_connection_state(self, result):
        logger.info("result {}".format(result))
        self.state.send("connection_sucess") if result is True else self.state.send(
            "connection_failure"
        )

    async def sleep(self, value: float):
        logger.info("Sleeping for {}s".format(value))
        time.sleep(value)
        return True

    @retry(times=3, exceptions=Exception)
    async def connect(self):
        """
        Establish connection between Module and client over TCP socket
        Returns
        -----------
        bool
         True on successul connection

        """

        response: Response
        try:
            response = await self._client.connect()
            logger.trace(response)
            if response.result:
                logger.info("connection to {} successful".format(self._module_name))
            else:
                logger.error(
                    "connection to {} {}".format(
                        self._module_name, str(response.message)
                    )
                )

        except Exception as e:
            logger.error("Error on connection {}".format(e))
            response = (False, "connect", "connection", str(e))
        return response

    async def disconnect(self) -> Response:
        """
        Disconnection between Module and client over TCP socket
        Returns
        -----------
        bool
         True on successful connection

        """
        result: Response = await self._client.close()
        logger.info(
            "disconnection to {} is {}".format(self._module_name, result.message)
        )
        return result
