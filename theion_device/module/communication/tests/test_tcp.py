import logging
import time
from asyncio import StreamReader
from unittest.mock import patch

import pytest

from theion_device.module.communication.src.response import Response
from theion_device.module.communication.src.tcp import TCPStreamClient


@pytest.mark.skiptest
@pytest.mark.asyncio
async def test_tcp():
    client = TCPStreamClient("127.0.0.1", 8882, 4096)
    result = await client.connect()
    assert isinstance(result, bool)
    assert result == True
    result = await client.send_message("Hello world")
    assert isinstance(result, bool)
    assert result == True
    message = await client.read_message_until()
    assert message == "Hello from server\r"


@pytest.mark.skiptest
@pytest.mark.asyncio
async def test_tcp_fail():
    client = TCPStreamClient("192.168.0.214", 8882, 4096)
    result = await client.connect()
    logging.info(result)
    # assert (isinstance(result, Exception))
    i = 0

    while True:
        result = await client.send_message("?")
        message = await client.read_message_until("\n")
        logging.info("result  {} {} {}".format(i, result, message))
        i = i + 1
        time.sleep(1)

    # assert(isinstance(result,Exception))


@pytest.mark.skiptest
@pytest.mark.asyncio
async def test_tcp_context():
    client: TCPStreamClient = TCPStreamClient("127.0.0.1", 8883, 4096)
    client1 = None
    async with client:
        logging.info(client)
        client1 = client


tcp = "theion_device.communication.theion_device.tcp."


@patch.object(TCPStreamClient, "send_message")
@patch.object(TCPStreamClient, "read_message_until")
@pytest.mark.asyncio
async def test_non_unicode_message(mock_receive_message, mock_send_message):
    non_unicode_state = (
        "<퟿������Idle|MPos:-200.000,5.000,0.000|FS:0,0|WCO:0.000,0.000,0.000>\n"
    )
    unicode_state = "<Idle|MPos:-200.000,5.000,0.000|FS:0,0|WCO:0.000,0.000,0.000>\n"
    client = TCPStreamClient("127.0.0.1", 8882, 4096)
    mock_send_message.return_value = Response(True, "", "", "")
    mock_receive_message.return_value = Response(False, "", "READ", UnicodeError())

    client.connected = True
    result = await client.send_message_ack("?\n", 1)
    logging.info("result {}".format(result))
    mock_receive_message.side_effect = [
        Response(False, "", "READ", UnicodeError()),
        Response(True, "", "READ", unicode_state),
    ]
    result = await client.send_message_ack("?\n", 1)
    logging.info("result {}".format(result))
