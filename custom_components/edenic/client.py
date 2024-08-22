"""
Client module for interacting with the Edenic API.
"""

import logging
from typing import Any

import aiohttp
from homeassistant.exceptions import HomeAssistantError

from .const import API_URL_BASE

_LOGGER = logging.getLogger(__name__)

HTTP_OK = 200


class EdenicClient:
    """Encapsulates HTTP calls to the Edenic API."""

    def __init__(self, api_key: str, organization_id: str) -> None:
        """

        Args:
        ----
            api_key: The API key for authenticating with the Edenic API.
            organization_id: The organization ID for the Edenic API.

        """
        self._api_key = api_key
        self._organization_id = organization_id

    async def get_devices(self) -> list[dict[str, Any]]:
        """Get a list of devices."""
        headers = self.__create_headers()
        try:
            async with (
                aiohttp.ClientSession() as session,
                session.get(f"{API_URL_BASE}/devices", headers=headers) as response,
            ):
                _LOGGER.debug("Response status: %s", response.status)
                _LOGGER.debug("Response content: %s", await response.text())
                if response.status != HTTP_OK:
                    error_message = "Failed to fetch devices"
                    _LOGGER.exception(error_message)
                    raise HomeAssistantError(error_message)
                return await response.json()
        except aiohttp.ClientError as e:
            error_message = "Client error"
            _LOGGER.exception(error_message)
            raise HomeAssistantError(error_message) from e
        except TimeoutError:
            error_message = "Request timed out"
            _LOGGER.exception(error_message)
            raise HomeAssistantError(error_message) from None

    async def get_device_telemetry(self, device_id: str) -> dict[str, Any]:
        """Get telemetry data for a device."""
        headers = self.__create_headers()
        try:
            async with (
                aiohttp.ClientSession() as session,
                session.get(
                    f"{API_URL_BASE}/telemetry/{device_id}", headers=headers
                ) as response,
            ):
                if response.status != HTTP_OK:
                    _LOGGER.exception("Failed to fetch telemetry: %s", response.status)
                    error_message = "Failed to fetch telemetry"
                    raise HomeAssistantError(error_message)
                return await response.json()
        except aiohttp.ClientError as e:
            error_message = "Client error"
            _LOGGER.exception(error_message)
            raise HomeAssistantError(error_message) from e
        except TimeoutError:
            error_message = "Request timed out"
            _LOGGER.exception(error_message)
            raise HomeAssistantError(error_message) from None

    async def get_device_attributes(
        self, device_id: str, keys: str | None = None
    ) -> dict[str, Any]:
        """Get attributes for a device."""
        headers = self.__create_headers()
        params = {"keys": keys} if keys else {}
        try:
            async with (
                aiohttp.ClientSession() as session,
                session.get(
                    f"{API_URL_BASE}/attributes/{device_id}",
                    headers=headers,
                    params=params,
                ) as response,
            ):
                if response.status != HTTP_OK:
                    _LOGGER.exception(
                        "Failed to fetch device attributes: %s", response.status
                    )
                    error_message = "Failed to fetch device attributes"
                    raise HomeAssistantError(error_message)
                return await response.json()
        except aiohttp.ClientError as e:
            error_message = "Client error"
            _LOGGER.exception(error_message)
            raise HomeAssistantError(error_message) from e
        except TimeoutError:
            error_message = "Request timed out"
            _LOGGER.exception(error_message)
            raise HomeAssistantError(error_message) from None

    def __create_headers(self) -> dict:
        """Create a header object to use in a request to the Edenic API."""
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

    async def fetch_devices(self) -> None:
        """Fetch devices from the API."""
        response = await self._make_request()
        if response.status != HTTP_OK:
            error_message = "Failed to fetch devices"
            _LOGGER.exception(error_message)
            raise HomeAssistantError(error_message)

    async def fetch_telemetry(self) -> None:
        """Fetch telemetry from the API."""
        response = await self._make_request()
        if response.status != HTTP_OK:
            error_message = "Failed to fetch telemetry"
            _LOGGER.exception(error_message)
            raise HomeAssistantError(error_message)

    async def fetch_device_attributes(self) -> None:
        """Fetch device attributes from the API."""
        response = await self._make_request()
        if response.status != HTTP_OK:
            error_message = "Failed to fetch device attributes"
            _LOGGER.exception(error_message)
            raise HomeAssistantError(error_message)

    async def _make_request(self) -> None:
        pass

    async def handle_client_error(self, e: Exception) -> None:
        """Handle client errors."""
        error_message = "Client error"
        _LOGGER.exception(error_message)
        raise HomeAssistantError(error_message) from e

    async def handle_timeout_error(self) -> None:
        """Handle timeout errors."""
        error_message = "Request timed out"
        _LOGGER.exception(error_message)
        raise HomeAssistantError(error_message) from None

    async def handle_errors(self) -> None:
        """Handle various errors."""
        try:
            await self._make_request()
        except aiohttp.ClientError as e:
            await self.handle_client_error(e)
