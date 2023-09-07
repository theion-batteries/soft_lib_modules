import logging

import pytest

from src.module.communication import Client, TCPStreamClient


@pytest.mark.skiptest
@pytest.mark.asyncio
async def test_sample_connection():
    client: Client = TCPStreamClient("127.0.0.1", 8881, 4096)
    await client.connect()
    await client.send_message("hello")


def test_get_confi_cache():
    logging.info(pytest.__dict__)


@pytest.mark.skiptest
@pytest.mark.asyncio
async def test_cnt_dispenser():
    client: Client = TCPStreamClient("192.168.0.203", 8881, 4096)
    result = await client.connect()
    assert result
    result = await client.send_message("off\r\n")
    assert result
    result = await client.read_message_until()
    assert result.message == "vibrator disabled"
    logging.info(result.message)
    result = await client.close()
    assert result


@pytest.mark.skiptest(reason="Need server running")
@pytest.mark.asyncio
async def test_whs_motion():
    client: Client = TCPStreamClient("192.168.0.214", 8882, 4096)
    result = await client.connect()
    assert result
    result = await client.send_message("?\n")
    logging.info(result)

    assert result
    result = await client.read_message_until()
    logging.info(result)
    result = await client.read_message_until()
    logging.info(result)
    result = await client.close()
    assert result
