import unittest
from unittest.mock import AsyncMock, Mock, patch

import httpx

from devopness.core.network_error import (
    DevopnessNetworkError,
    handle_network_errors,
    handle_network_errors_sync,
)


class TestDevopnessNetworkError(unittest.IsolatedAsyncioTestCase):
    @patch("httpx.AsyncClient.get", new_callable=AsyncMock)
    async def test_devopness_network_error(self, mock_get: AsyncMock) -> None:
        request = httpx.Request("GET", "https://host.invalid/")
        mock_get.side_effect = httpx.ConnectError(
            "[Errno -2] Name or service not known", request=request
        )

        @handle_network_errors
        async def failing_request() -> httpx.Response:
            async with httpx.AsyncClient() as client:
                return await client.get("https://host.invalid/")

        with self.assertRaises(DevopnessNetworkError) as context:
            await failing_request()

        error = context.exception

        assert error.url == "https://host.invalid/"
        assert error.method == "GET"

        assert isinstance(error.exception, httpx.RequestError)

        string_output = str(error)
        assert (
            "\nDevopness SDK Error: Network Request Failed\n\n"
            "Request: GET https://host.invalid/\n"
            "Exception: [Errno"
        ) in string_output

    @patch("httpx.Client.get")
    def test_devopness_network_error_sync(self, mock_get: Mock) -> None:
        request = httpx.Request("GET", "https://host.invalid/")
        mock_get.side_effect = httpx.ConnectError(
            "[Errno -2] Name or service not known", request=request
        )

        @handle_network_errors_sync
        def failing_request_sync() -> httpx.Response:
            with httpx.Client() as client:
                return client.get("https://host.invalid/")

        with self.assertRaises(DevopnessNetworkError) as context:
            failing_request_sync()

        error = context.exception

        assert error.url == "https://host.invalid/"
        assert error.method == "GET"

        assert isinstance(error.exception, httpx.RequestError)

        string_output = str(error)
        assert (
            "\nDevopness SDK Error: Network Request Failed\n\n"
            "Request: GET https://host.invalid/\n"
            "Exception: [Errno"
        ) in string_output
