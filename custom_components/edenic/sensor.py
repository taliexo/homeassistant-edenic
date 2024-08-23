"""Support for Edenic sensors."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfTemperature
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util.unit_conversion import TemperatureConverter

from .const import (
    DOMAIN, SENSOR_TYPES, ATTR_DEVICE_ID, ATTR_DEVICE_NAME, ATTR_DEVICE_TYPE,
    CONF_TEMP_UNIT, CONF_CONDUCTIVITY_UNIT, CONDUCTIVITY_UNIT_MS,
    CONDUCTIVITY_UNIT_US, CONDUCTIVITY_UNIT_PPM_500, CONDUCTIVITY_UNIT_PPM_700,
    MS_TO_US, PPM_500_FACTOR, PPM_700_FACTOR, DEFAULT_TEMP_UNIT, DEFAULT_CONDUCTIVITY_UNIT
)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Edenic sensors based on a config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    temp_unit = config_entry.options.get(CONF_TEMP_UNIT, config_entry.data.get(CONF_TEMP_UNIT, DEFAULT_TEMP_UNIT))
    conductivity_unit = config_entry.options.get(CONF_CONDUCTIVITY_UNIT, config_entry.data.get(CONF_CONDUCTIVITY_UNIT, DEFAULT_CONDUCTIVITY_UNIT))

    entities = []
    for device in coordinator.data:
        for sensor_type in SENSOR_TYPES:
            entities.append(EdenicSensor(coordinator, device, sensor_type, temp_unit, conductivity_unit))

    async_add_entities(entities)

class EdenicSensor(CoordinatorEntity, SensorEntity):
    """Representation of an Edenic sensor."""

    def __init__(self, coordinator, device, sensor_type, temp_unit, conductivity_unit):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._sensor_type = sensor_type
        self._temp_unit = temp_unit
        self._conductivity_unit = conductivity_unit
        self._attr_unique_id = f"{device['id']}_{sensor_type}"
        self._attr_name = f"{device['label']} {SENSOR_TYPES[sensor_type]['name']}"
        self._attr_device_class = SENSOR_TYPES[sensor_type].get('device_class')
        self._attr_icon = SENSOR_TYPES[sensor_type]['icon']

        self._update_units()

    def _update_units(self):
        """Update the units based on the current settings."""
        if self._sensor_type == 'temperature':
            self._attr_native_unit_of_measurement = self._temp_unit
        elif self._sensor_type == 'electrical_conductivity':
            self._attr_native_unit_of_measurement = self._conductivity_unit
        else:
            self._attr_native_unit_of_measurement = SENSOR_TYPES[self._sensor_type].get('unit')

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.coordinator.data:
            device_data = next((d for d in self.coordinator.data if d['id'] == self._device['id']), None)
            if device_data and self._sensor_type in device_data:
                value = device_data[self._sensor_type][0]['value']
                if self._sensor_type == 'temperature':
                    return self.convert_temperature(float(value))
                elif self._sensor_type == 'electrical_conductivity':
                    return self.convert_conductivity(float(value))
                return value
        return None

    def convert_temperature(self, value):
        """Convert temperature if necessary."""
        if self._temp_unit == UnitOfTemperature.FAHRENHEIT:
            return round(TemperatureConverter.convert(value, UnitOfTemperature.CELSIUS, UnitOfTemperature.FAHRENHEIT), 2)
        return round(value, 2)

    def convert_conductivity(self, value):
        """Convert conductivity to the desired unit."""
        # Assuming the API returns values in mS/cm
        if self._conductivity_unit == CONDUCTIVITY_UNIT_MS:
            return round(value, 2)
        elif self._conductivity_unit == CONDUCTIVITY_UNIT_US:
            return round(value * MS_TO_US, 2)
        elif self._conductivity_unit == CONDUCTIVITY_UNIT_PPM_500:
            return round(value * MS_TO_US * PPM_500_FACTOR / 1000, 2)
        elif self._conductivity_unit == CONDUCTIVITY_UNIT_PPM_700:
            return round(value * MS_TO_US * PPM_700_FACTOR / 1000, 2)

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            ATTR_DEVICE_ID: self._device['id'],
            ATTR_DEVICE_NAME: self._device['label'],
            ATTR_DEVICE_TYPE: self._device['additionalInfo']['deviceSubType'],
        }

    async def async_update(self):
        """Update the entity."""
        await super().async_update()
        self._update_units()