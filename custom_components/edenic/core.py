"""Core module for the Edenic integration."""

import logging
from datetime import UTC, datetime, timedelta
from typing import Any

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from custom_components.edenic.client import EdenicClient

_LOGGER = logging.getLogger(__name__)

TIMEOUT_THRESHOLD = 60  # Define the TIMEOUT_THRESHOLD constant
POLLING_INTERVAL = 60  # Fixed polling interval in seconds


class EdenicService:
    """Service layer object responsible for initializing and updating values from the Edenic API."""

    def __init__(self, api_key: str) -> None:
        """Initialize the service."""
        self._client = EdenicClient(api_key)
        self._last_telemetry_call = None

    def should_update_telemetry(self) -> bool:
        """Determine if telemetry should be updated."""
        if self._last_telemetry_call is None:
            return True
        return (
            datetime.now(UTC) - self._last_telemetry_call
        ).total_seconds() > TIMEOUT_THRESHOLD

    async def get_device_attributes(
        self, device_id: str, keys: str | None = None
    ) -> dict[str, Any]:
        """Get attributes for a device."""
        return await self._client.get_device_attributes(device_id, keys)

    async def update_device_attributes(
        self, device_id: str, attributes: dict
    ) -> dict[str, Any]:
        """Update attributes for a device."""
        return await self._client.update_device_attributes(device_id, attributes)


class EdenicDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, service: EdenicService) -> None:
        """Initialize the data update coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="Edenic",
            update_interval=timedelta(seconds=POLLING_INTERVAL),
        )
        self._edenic = service

    async def _async_update_data(self) -> None:
        """Fetch data from the Edenic API."""
        _LOGGER.debug("Refreshing data from Edenic API")
        await self._edenic.refresh()
        return self._edenic

    @property
    def edenic(self) -> EdenicService:
        """Return the underlying Edenic API object from the assigned coordinator."""
        return self._edenic


class EdenicEntity(CoordinatorEntity[EdenicDataUpdateCoordinator]):
    """Representation of an Edenic entity."""

    _attr_has_entity_name = True

    def __init__(
        self, coordinator: EdenicDataUpdateCoordinator, data_key: str, platform: str
    ) -> None:
        """Initialize the Edenic entity."""
        self._coordinator = coordinator
        self._data_key = data_key
        self._platform = platform

    @property
    def edenic(self) -> EdenicService:
        """Return the underlying Edenic API object from the assigned coordinator."""
        return self.coordinator.edenic

    @property
    def platform_name(self) -> str:
        """Return the platform name."""
        return self._platform
