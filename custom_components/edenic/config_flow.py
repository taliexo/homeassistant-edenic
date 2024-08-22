"""Config flow for Edenic integration."""
import logging
from typing import Any, Dict, Optional

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import EdenicApiClient, EdenicApiError
from .const import DOMAIN, CONF_API_KEY, CONF_ORGANIZATION_ID

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

class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""

class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""