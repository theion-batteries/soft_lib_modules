from unittest.mock import patch

import pytest

from ..src.keyence import KeyenceClient
from ..src.response import Response


#
@patch.object(KeyenceClient, "close")
@patch.object(KeyenceClient, "connect")
@pytest.mark.asyncio
async def test_keyence_valid_data(mock_connect, mock_close):
    mock_connect.return_value = Response(True, "", "CONNECTION", "RC_OK")

    mock_close.return_value = Response(True, "", "DISCONNECTION", "RC_OK")
    client = KeyenceClient("127.0.0.1", 8883, 4096)

    response = await client.connect()
    assert response.result
