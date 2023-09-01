import asyncio
import time
from typing import Optional

from definitions import logger

from .client import Client
from .exception_handler import (
    StreamExceptionHandler,
    StreamReadExceptionHandler,
    TCPClientException,
)
from .response import Response
from .retry import retry


class TCPStreamClient(Client):
    def __init__(self, ip: str, port: int, buffer_size: int):
        self.__ip = ip
        self.__port = port
        self.__buffer_size = buffer_size
        self.__reader: Optional[asyncio.StreamReader] = None
        self.__writer: Optional[asyncio.StreamWriter] = None
        self.__retry_max = 3
        self.connected = False

    @StreamExceptionHandler
    async def __aenter__(self):
        logger.info("Entering context ")
        return self

    @StreamExceptionHandler
    async def __aexit__(self, exc_type, exc_value, exc_traceback):
        logger.info("Exiting context ")
        result = await self.close()
        return result

    @StreamExceptionHandler
    async def connect(self) -> bool | Exception:
        self.__reader, self.__writer = await asyncio.open_connection(
            self.__ip, self.__port, limit=self.__buffer_size
        )
        await self.check_connection()

    @retry(times=3, exceptions=TCPClientException)
    async def reconnect(self):
        """attempts to reconnect to the module if the connection is lost. for three time0

        Returns
        ----------
        Response

        """
        logger.trace("Attempting to reconnect ....")
        time.sleep(5)
        await self.close()
        response = await self.connect()
        logger.trace("Result of reconnect {}".format(response.message))
        if response.result:
            self.change_state(True)
        return response

    def change_state(self, connected):
        self.connected = connected

    async def check_connection(self) -> bool | Exception:
        """Check whether the connection exist or not

        Returns
        ----------
        bool | Exception

        """
        message = "Connection to {}:{}".format(self.__ip, self.__port)
        if self.__writer is None or self.__reader is None:
            logger.trace("{} does not exist".format(message))
            self.change_state(False)
        elif self.__writer.is_closing():
            logger.trace("{} is closed".format(message))
            await self.close()
            self.change_state(False)
        else:
            self.change_state(True)

    @StreamExceptionHandler
    async def send_message(self, data) -> bool | Exception:
        logger.trace("sent message {}".format(data.encode()))
        await self.check_connection()
        if not self.connected:
            await self.reconnect()
        if self.connected:
            self.__writer.write(data.encode())
            await self.__writer.drain()

    @StreamReadExceptionHandler
    async def read_message_until(self, delimiter: str = "\n") -> str | Exception:
        await self.check_connection()
        if not self.connected:
            await self.reconnect()
        result = await self.__reader.readuntil(delimiter.encode())
        return result

    @StreamReadExceptionHandler
    async def read_message_n(self, no_of_bytes: int) -> str | Exception:
        await self.check_connection()
        if not self.connected:
            await self.reconnect()
        async with asyncio.timeout(10):
            return await self.__reader.readexactly(no_of_bytes)

    @StreamReadExceptionHandler
    async def read_message(self) -> str:
        await self.check_connection()
        if not self.connected:
            await self.reconnect()

        result = await self.__reader.read(self.__buffer_size)
        return result

    async def read_message_line(self) -> str:
        await self.check_connection()
        if not self.connected:
            await self.reconnect()

        data = await self.__reader.readline()
        return data.decode()

    @retry(3, exceptions=(TimeoutError, UnicodeError))
    async def send_message_ack(
        self, command: str, number_of_response: int, timeout: int = 10
    ) -> Response:
        """
        Sends command and waits for it to be acknowledged ("ok" or "error")
        Most messages sent, reply with an acknowledgment message (usually 'ok')
        with this method we can assert the message was received and processed

        Parameters
        ---------------
        command: str
            message to be sent to remote grbl module
        number_of_response: int
            module send back one, two or three messages back to the client based on the command and type of the module

        Returns
        ----------------
        Response

        """
        assert number_of_response >= 0
        send_response: Response = None
        receive_response: list[Response] = list()
        send_timeout = 10
        try:
            async with asyncio.timeout(timeout):
                send_response = await self.send_message(command)
            logger.trace(send_response)
            if not send_response.result:
                logger.error(
                    "Error: ".format(send_response)
                )  # TODO decide what to do after error
                raise send_response.message
            else:

                async def read_with_timeout():
                    async with asyncio.timeout(timeout):
                        response = await self.read_message_until()
                        logger.trace(response)

                        response.command = command
                        return response

                for counter in range(0, number_of_response):
                    response = await read_with_timeout()
                    if not response.result:
                        raise response.message
                    receive_response.append(response)
        except asyncio.TimeoutError as e:
            logger.error("Timeout error {}".format(repr(e)))
            await self.close()  # In case of timeout
            await self.connect()
            receive_response = [Response(False, command, "", repr(e))]

        except UnicodeError as e:
            logger.error("Unicode error {}".format(repr(e)))
            receive_response = [Response(False, command, "", repr(e))]

        except Exception as e:
            receive_response = [Response(False, command, "", repr(e))]

        return receive_response

    @StreamExceptionHandler
    async def close(self):
        response: Response = Response(
            False, "", "DISCONNECTION", "Connection dont exist"
        )

        if self.__writer is not None:
            self.__writer.close()
            await self.__writer.wait_closed()
            self.__reader = None
            self.__writer = None
            response = Response(True, "", "DISCONNECTION", "Successful")

        return response
