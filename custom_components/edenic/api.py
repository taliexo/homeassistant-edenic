"""API client for Edenic."""
import aiohttp
import async_timeout
import asyncio
from .const import API_BASE_URL

class EdenicApiClient:
    """API client for Edenic."""

    def __init__(self, api_key, organization_id, session):
        """Initialize the API client."""
        self._api_key = api_key
        self._organization_id = organization_id
        self._session = session

    async def async_get_devices(self):
        """Get list of devices."""
        url = f"{API_BASE_URL}/device/{self._organization_id}"
        return await self._api_request("GET", url)

    async def async_get_latest_telemetry(self, device_id):
        """Get latest telemetry for a device."""
        url = f"{API_BASE_URL}/telemetry/{device_id}"
        return await self._api_request("GET", url)

    async def _api_request(self, method, url, data=None):
        """Make an API request with retry logic in case of rate limit."""
        headers = {"Authorization": self._api_key}
        max_retries = 10
        retry_delay = 2  # initial delay in seconds

        for attempt in range(max_retries):
            try:
                async with async_timeout.timeout(10):
                    async with self._session.request(method, url, headers=headers, json=data) as resp:
                        resp.raise_for_status()
                        return await resp.json()
            except aiohttp.ClientResponseError as err:
                if err.status == 400 and attempt < max_retries - 1:
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2  # exponential backoff
                else:
                    raise EdenicApiError(f"Error communicating with API: {err}")
            except aiohttp.ClientError as err:
                raise EdenicApiError(f"Error communicating with API: {err}")

class EdenicApiError(Exception):
    """Raised when there is an error with the Edenic API."""