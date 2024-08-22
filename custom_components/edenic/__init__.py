"""The Edenic integration."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant

from .const import DOMAIN, PLATFORMS
from .core import EdenicDataUpdateCoordinator, EdenicService

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Edenic from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    service = EdenicService(entry.data["api_key"])
    coordinator = EdenicDataUpdateCoordinator(hass, service)

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await coordinator.async_config_entry_first_refresh()
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
