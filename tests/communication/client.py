import asyncio
import atexit
import socket
from asyncio import Transport
from datetime import datetime
from typing import Optional


class TCPStreamClient:
    def __init__(self, ip: str, port: int):
        self.__ip = ip
        self.__port = port
        self.__reader: Optional[asyncio.StreamReader] = None
        self.__writer: Optional[asyncio.StreamWriter] = None

    async def connect(self):
        self.__reader, self.__writer = await asyncio.open_connection(
            self.__ip, self.__port
        )

    async def send_message(self, data):
        self.__writer.write(data.encode())
        await self.__writer.drain()

    async def read_message(self) -> str:
        data = await self.__reader.readuntil()
        return data.decode()

    async def close(self):
        self.__writer.close()
        await self.__writer.wait_closed()


async def test_sample_connection():
    loop = asyncio.get_running_loop()
    rsock, wsock = socket.socketpair()
    print(rsock, wsock)
    reader, writer = await asyncio.open_connection(sock=rsock)
    loop.call_soon(wsock.send, "abc".encode())

    client = TCPStreamClient("127.0.0.1", 8882)
    await client.connect()
    await client.send_message("Hello world\n")
    print(await client.read_message())


asyncio.run(test_sample_connection())
