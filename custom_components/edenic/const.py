"""Constants for the Edenic integration."""
DOMAIN = "edenic"

CONF_API_KEY = "api_key"
CONF_ORGANIZATION_ID = "organization_id"

DEFAULT_SCAN_INTERVAL = 120

ATTR_DEVICE_ID = "device_id"
ATTR_DEVICE_NAME = "device_name"
ATTR_DEVICE_TYPE = "device_type"

SENSOR_TYPES = {
    "temperature": {
        "key": "temperature",
        "name": "Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
    },
    "electrical_conductivity": {
        "key": "electrical_conductivity",
        "name": "Electrical Conductivity",
        "unit": "mS/cm",
        "icon": "mdi:flash",
    },
    "ph": {
        "key": "ph",
        "name": "pH",
        "unit": None,
        "icon": "mdi:test-tube",
    },
}

API_BASE_URL = "https://api.edenic.io/api/v1"