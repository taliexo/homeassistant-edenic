"""The Edenic integration."""
import asyncio
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import EdenicApiClient, EdenicApiError
from .const import (
    DOMAIN, CONF_API_KEY, CONF_ORGANIZATION_ID, CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL, CONF_TEMP_UNIT, DEFAULT_TEMP_UNIT,
    CONF_CONDUCTIVITY_UNIT, DEFAULT_CONDUCTIVITY_UNIT
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Edenic from a config entry."""
    api_key = entry.data[CONF_API_KEY]
    organization_id = entry.data[CONF_ORGANIZATION_ID]

    # Use options if set, otherwise use defaults
    scan_interval = entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
    temp_unit = entry.options.get(CONF_TEMP_UNIT, DEFAULT_TEMP_UNIT)
    conductivity_unit = entry.options.get(CONF_CONDUCTIVITY_UNIT, DEFAULT_CONDUCTIVITY_UNIT)

    session = async_get_clientsession(hass)
    client = EdenicApiClient(api_key, organization_id, session)

    coordinator = EdenicDataUpdateCoordinator(hass, client=client, update_interval=scan_interval)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(update_listener))

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok

async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update listener."""
    await hass.config_entries.async_reload(entry.entry_id)

class EdenicDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Edenic data."""

    def __init__(self, hass: HomeAssistant, client: EdenicApiClient, update_interval: int):
        """Initialize the data update coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=update_interval),
        )
        self.client = client

    async def _async_update_data(self):
        """Fetch data from Edenic."""
        try:
            devices = await self.client.async_get_devices()
            data = []
            for device in devices:
                telemetry = await self.client.async_get_latest_telemetry(device['id'])
                device_data = {**device, **telemetry}
                data.append(device_data)
            return data
        except EdenicApiError as err:
            raise UpdateFailed(f"Error communicating with API: {err}")