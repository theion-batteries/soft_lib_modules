import ctypes
from enum import Enum

from soft_lib_modules.definitions import logger

from ..src.response import Response
from .client import Client
from .dll import get_keyence_lib


class KeyenceResult(Enum):
    RC_NOT_OK = -1.0
    LKIF_FLOATRESULT_INVALID = -2.0
    LKIF_FLOATRESULT_ALARM = -3.0
    LKIF_FLOATRESULT_RANGEOVER_N = -4.0
    LKIF_FLOATRESULT_RANGEOVER_P = -5.0
    LKIF_FLOATRESULT_WAITING = -6.0


class KeyenceClient(Client):
    def __init__(self, ip: str, port: int, buffer_size: int):
        self.__keyence_lib = get_keyence_lib()

        self.__ip = ip
        self.__current_distance = 0.0
        self.__current_state = ""
        self.__valid_state = "RC_OK"  # defined by Keyence C++ API
        self.__disconnected_state = "RC_DISCONNECTED"

    async def connect(self) -> bool | Exception:
        result: Response = None
        self.__current_state = self.__keyence_lib.keyence_connect(self.__ip)
        logger.trace(
            "Keyence client connection feedback {}".format(self.__current_state)
        )
        connected = self.__current_state == self.__valid_state
        result = Response(connected, "", "CONNECTION", self.__current_state)
        logger.trace("Keyence connection {}".format(result))
        return result

    async def send_message(self, data) -> Response:
        result: Response = None
        if not self.__current_state == self.__valid_state:
            result = Response(False, data, "SEND", self.__current_state)
        else:
            self.__current_distance = self.__keyence_lib.get_data()
            self.__current_state = self.__keyence_lib.keyence_get_current_state()
            is_valid_state = self.__current_state == self.__valid_state

            result = Response(is_valid_state, "?", "SEND", self.__current_state)

            if not result.result:
                logger.error(
                    "Keyence Controller is not connected due to {}".format(
                        self.__current_state
                    )
                )

        return result

    async def read_message_until(self, delimiter: str = "\n") -> Response:
        result: Response = None
        is_valid_state = self.__current_state == self.__valid_state
        result = Response(is_valid_state, "?", "READ", self.__current_distance)
        if not result.result:
            logger.error(
                "Keyence Controller is not connected due to {}".format(
                    self.__current_state
                )
            )
        return result

    async def read_message(self) -> float:
        return await self.read_message_until()

    async def read_message_line(self) -> float:
        return await self.read_message_until()

    async def close(self) -> bool | Exception:
        result: Response
        self.__current_state = self.__keyence_lib.keyence_disconnect(self.__ip)
        logger.trace(
            "Keyence client disconnection feedback {}".format(self.__current_state)
        )

        if self.__current_state == self.__disconnected_state:
            result = Response(True, "", "DISCONNECTION", "Success")
        else:
            result = Response(False, "", "DISCONNECTION", self.__current_state)

        return result
