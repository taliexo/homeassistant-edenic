"""Support for Edenic sensors."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, SENSOR_TYPES, ATTR_DEVICE_ID, ATTR_DEVICE_NAME, ATTR_DEVICE_TYPE

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Edenic sensors based on a config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities = []
    for device in coordinator.data:
        for sensor_type in SENSOR_TYPES:
            entities.append(EdenicSensor(coordinator, device, sensor_type))

    async_add_entities(entities)

class EdenicSensor(CoordinatorEntity, SensorEntity):
    """Representation of an Edenic sensor."""

    def __init__(self, coordinator, device, sensor_type):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._sensor_type = sensor_type
        self._attr_unique_id = f"{device['id']}_{sensor_type}"
        self._attr_name = f"{device['label']} {SENSOR_TYPES[sensor_type]['name']}"
        self._attr_device_class = SENSOR_TYPES[sensor_type].get('device_class')
        self._attr_native_unit_of_measurement = SENSOR_TYPES[sensor_type]['unit']
        self._attr_icon = SENSOR_TYPES[sensor_type]['icon']

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.coordinator.data:
            device_data = next((d for d in self.coordinator.data if d['id'] == self._device['id']), None)
            if device_data and self._sensor_type in device_data:
                return device_data[self._sensor_type][0]['value']
        return None

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            ATTR_DEVICE_ID: self._device['id'],
            ATTR_DEVICE_NAME: self._device['label'],
            ATTR_DEVICE_TYPE: self._device['additionalInfo']['deviceSubType'],
        }