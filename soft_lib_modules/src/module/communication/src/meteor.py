import ctypes
from abc import ABC, abstractmethod

from soft_lib_modules.definitions import logger

from ..src.response import Response
from .client import Client
from .dll import get_meteor_lib


class MeteorClient:
    """Python API to communicate with  Meteor SDK"""

    def __init__(self, ip: str = "", port: int = 0, buffer_size: int = 0):
        # Meteor API works with Ethernet. The name of the Ethernet adapter is configured in the config file.
        self.__meteor_lib = get_meteor_lib()

    def connect(self) -> bool | Exception:
        """ """
        pass

    def set_parameter(self, file_name, frequency, no_of_copies):
        self.__file_name = file_name
        self.__frequency = frequency
        self.__no_of_copies = no_of_copies

    def is_parameter_set(self):
        return self.__file_name != "" and self.__file_name

    def send_message(self, data: str) -> bool | Exception:
        """send message to the client

        Parameters
        -------------
        data: str

        Returns
        --------
        bool | Exception

        """
        response: Response = Response(True, data, "", "")
        try:
            if data == "init":
                result = self.__meteor_lib.initialize_printer(
                    self.__file_name, self.__frequency, self.__no_of_copies
                )

            elif data == "trigger":
                result = self.__meteor_lib.trigger()

            elif data == "upload":
                result = self.__meteor_lib.upload_image(
                    self.__file_name, self.__no_of_copies
                )

            elif data == "close":
                result = self.__meteor_lib.stop_printer()
            logger.trace("meteor client response {}".format(result))

            response = Response(True, data, "", result.decode())

            if result.decode() != "RVAL_OK":
                response.result = False

        except Exception as e:
            logger.error("exception {}".format(str(e)))
            response.result = False
            response.message = str(e)

        return response

    def read_message_until(self, delimiter: str = "\n") -> str | Exception:
        """read message until delimiter is found

        Parameters
        ----------
        delimeter : str


        Returns
        --------
        str | Exception

        """

        pass

    def read_message(self) -> str:
        pass

    def read_message_line(self) -> str:
        pass

    def close(self):
        """close the connection"""

        pass
