import asyncio
from typing import Optional

import serial_asyncio

from .client import Client
from .exception_handler import StreamExceptionHandler, StreamReadExceptionHandler


class SerialStreamClient(Client):
    def __init__(self, ip: str, port: int, buffer_size: int):
        self.__ip = ip
        self.__port = port
        self.__buffer_size = buffer_size
        self.__reader: Optional[asyncio.StreamReader] = None
        self.__writer: Optional[asyncio.StreamWriter] = None

    @StreamExceptionHandler
    async def __aenter__(self):
        return self

    @StreamExceptionHandler
    async def __aexit__(self, exc_type, exc_value, exc_traceback):
        self.__writer.close()
        await self.__writer.wait_closed()

    @StreamExceptionHandler
    async def connect(self) -> bool | Exception:
        self.__reader, self.__writer = await serial_asyncio.open_serial_connection(
            self.__ip, self.__port
        )

    @StreamExceptionHandler
    async def send_message(self, data) -> bool | Exception:
        self.__writer.write(data.encode())
        await self.__writer.drain()

    @StreamReadExceptionHandler
    async def read_message_until(self, delimiter: str = "\n") -> str | Exception:
        return await self.__reader.readuntil(delimiter.encode())

    @StreamReadExceptionHandler
    async def read_message_n(self, no_of_bytes: int) -> str | Exception:
        return await self.__reader.readexactly(no_of_bytes)

    @StreamReadExceptionHandler
    async def read_message(self) -> str:
        return await self.__reader.read(self.__buffer_size)

    async def read_message_line(self) -> str:
        data = await self.__reader.readline()
        return data.decode()

    @StreamExceptionHandler
    async def close(self):
        self.__writer.close()
        await self.__writer.wait_closed()
