"""Constants for the Edenic integration."""
from homeassistant.const import UnitOfTemperature

DOMAIN = "edenic"

CONF_API_KEY = "api_key"
CONF_ORGANIZATION_ID = "organization_id"
CONF_TEMP_UNIT = "temperature_unit"
CONF_CONDUCTIVITY_UNIT = "conductivity_unit"
CONF_SCAN_INTERVAL = "scan_interval"

DEFAULT_SCAN_INTERVAL = 60
MIN_SCAN_INTERVAL = 60
DEFAULT_TEMP_UNIT = UnitOfTemperature.FAHRENHEIT
DEFAULT_CONDUCTIVITY_UNIT = "mS/cm"

ATTR_DEVICE_ID = "device_id"
ATTR_DEVICE_NAME = "device_name"
ATTR_DEVICE_TYPE = "device_type"

# Conductivity units
CONDUCTIVITY_UNIT_MS = "mS/cm"
CONDUCTIVITY_UNIT_US = "μS/cm"
CONDUCTIVITY_UNIT_PPM_500 = "ppm 500"
CONDUCTIVITY_UNIT_PPM_700 = "ppm 700"

# Conversion factors
MS_TO_US = 1000
PPM_500_FACTOR = 500
PPM_700_FACTOR = 700

SENSOR_TYPES = {
    "temperature": {
        "key": "temperature",
        "name": "Temperature",
        "icon": "mdi:thermometer",
    },
    "electrical_conductivity": {
        "key": "electrical_conductivity",
        "name": "Electrical Conductivity",
        "icon": "mdi:flash",
    },
    "ph": {
        "key": "ph",
        "name": "pH",
        "unit": "pH",
        "icon": "mdi:test-tube",
    },
}

API_BASE_URL = "https://api.edenic.io/api/v1"