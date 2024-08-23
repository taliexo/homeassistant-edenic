"""Config flow for Edenic integration."""
import logging
from typing import Any, Dict, Optional

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import EdenicApiClient, EdenicApiError
from .const import (
    DOMAIN, CONF_API_KEY, CONF_ORGANIZATION_ID, CONF_TEMP_UNIT,
    CONF_CONDUCTIVITY_UNIT, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL,
    MIN_SCAN_INTERVAL, DEFAULT_TEMP_UNIT, DEFAULT_CONDUCTIVITY_UNIT,
    CONDUCTIVITY_UNIT_MS, CONDUCTIVITY_UNIT_US, CONDUCTIVITY_UNIT_PPM_500,
    CONDUCTIVITY_UNIT_PPM_700
)

_LOGGER = logging.getLogger(__name__)

class EdenicConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Edenic."""

    VERSION = 1

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: Dict[str, str] = {}
        if user_input is not None:
            try:
                await self.validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title="Edenic", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_API_KEY): str,
                    vol.Required(CONF_ORGANIZATION_ID): str,
                }
            ),
            errors=errors,
        )

    async def validate_input(self, hass: HomeAssistant, data: Dict[str, Any]) -> None:
        """Validate the user input allows us to connect."""
        session = async_get_clientsession(hass)
        client = EdenicApiClient(data[CONF_API_KEY], data[CONF_ORGANIZATION_ID], session)

        try:
            await client.async_get_devices()
        except EdenicApiError as err:
            _LOGGER.error("Error occurred: %s", err)
            raise CannotConnect from err

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return EdenicOptionsFlowHandler(config_entry)

class EdenicOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle Edenic options."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_TEMP_UNIT,
                        default=self.config_entry.options.get(CONF_TEMP_UNIT, DEFAULT_TEMP_UNIT)
                    ): vol.In([UnitOfTemperature.CELSIUS, UnitOfTemperature.FAHRENHEIT]),
                    vol.Optional(
                        CONF_CONDUCTIVITY_UNIT,
                        default=self.config_entry.options.get(CONF_CONDUCTIVITY_UNIT, DEFAULT_CONDUCTIVITY_UNIT)
                    ): vol.In([CONDUCTIVITY_UNIT_MS, CONDUCTIVITY_UNIT_US, CONDUCTIVITY_UNIT_PPM_500, CONDUCTIVITY_UNIT_PPM_700]),
                    vol.Optional(
                        CONF_SCAN_INTERVAL,
                        default=self.config_entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
                    ): vol.All(int, vol.Range(min=MIN_SCAN_INTERVAL)),
                }
            ),
        )

class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""

class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""