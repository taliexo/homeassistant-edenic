"""API client for Edenic."""
import aiohttp
import async_timeout
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
        """Make an API request."""
        headers = {"Authorization": self._api_key}

        try:
            async with async_timeout.timeout(10):
                async with self._session.request(method, url, headers=headers, json=data) as resp:
                    resp.raise_for_status()
                    return await resp.json()
        except aiohttp.ClientError as err:
            raise EdenicApiError(f"Error communicating with API: {err}")

class EdenicApiError(Exception):
    """Raised when there is an error with the Edenic API."""