import time

import pytest

from theion_device.module.communication.src.client import Client
from theion_device.module.communication.src.keyence import KeyenceClient
from theion_device.util import logger


@pytest.mark.skiptest
@pytest.mark.asyncio
async def test_keyence_client():
    client: Client = KeyenceClient("192.168.0.104", 8882, 4096)
    result = await client.connect()
    assert result

    while True:
        await client.send_message("?\n")

        # logger.trace("result {}".format(result))
        result = await client.read_message_until()
        time.sleep(1)
        if result == 0.0:
            logger.trace("Keyence data received zero here : {}".format(result))
            break
        logger.trace("Keyence data: {}".format(result))
