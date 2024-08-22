"""Sensor module for the Edenic integration."""

import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .core import EdenicDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Edenic sensors based on a config entry."""
    coordinator: EdenicDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    devices = await coordinator.edenic.get_devices()

    entities = [
        EdenicSensor(coordinator, device["id"], key)
        for device in devices
        for key in ["temperature", "electrical_conductivity", "ph"]
        if key in await coordinator.edenic.get_device_telemetry(device["id"])
    ]

    # Add device attribute sensors
    for device in devices:
        device_id = device["id"]
        attributes = await coordinator.edenic.get_device_attributes(device_id)
        entities.extend(
            EdenicDeviceAttributeSensor(coordinator, device_id, key)
            for key in attributes
        )

    async_add_entities(entities, update_before_add=True)


class EdenicSensor(CoordinatorEntity, SensorEntity):
    """Representation of an Edenic sensor."""

    def __init__(
        self, coordinator: EdenicDataUpdateCoordinator, device_id: str, key: str
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device_id = device_id
        self._key = key
        self._attr_name = f"Edenic {key} Sensor"
        self._attr_unique_id = f"{device_id}_{key}"
        self._state = None

    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""
        try:
            telemetry = await self.coordinator.edenic.get_device_telemetry(
                self._device_id
            )
            self._state = telemetry.get(self._key, None)
        except Exception:
            _LOGGER.exception("Error fetching telemetry data")
            self._state = None

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self._state

    @property
    def device_info(self) -> dict:
        """Return device information about this sensor."""
        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": self._attr_name,
            "manufacturer": "Edenic",
        }


class EdenicDeviceAttributeSensor(CoordinatorEntity, SensorEntity):
    """Representation of an Edenic device attribute sensor."""

    def __init__(
        self, coordinator: EdenicDataUpdateCoordinator, device_id: str, key: str
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device_id = device_id
        self._key = key
        self._attr_name = f"Edenic {key} Attribute"
        self._attr_unique_id = f"{device_id}_{key}_attribute"
        self._state = None

    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""
        try:
            attributes = await self.coordinator.edenic.get_device_attributes(
                self._device_id
            )
            self._state = attributes.get(self._key, None)
        except Exception:
            _LOGGER.exception("Error fetching device attributes")
            self._state = None

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self._state

    @property
    def device_info(self) -> dict:
        """Return device information about this sensor."""
        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": self._attr_name,
            "manufacturer": "Edenic",
        }
