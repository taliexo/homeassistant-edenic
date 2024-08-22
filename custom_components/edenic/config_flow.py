"""Config flow for Edenic integration."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

import voluptuous as vol
from homeassistant import config_entries

if TYPE_CHECKING:
    from homeassistant.helpers.typing import FlowResult

from custom_components.edenic.client import EdenicClient
from custom_components.edenic.const import (
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required("api_key"): str,
        vol.Required("organization_id"): str
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Edenic."""

    VERSION = 1

    @staticmethod
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create the options flow."""
        return OptionsFlow(config_entry)

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                client = EdenicClient(
                    user_input["api_key"], user_input["organization_id"]
                )
                await client.get_devices()
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "cannot_connect"
            else:
                await self.async_set_unique_id(f"edenic-{user_input['api_key']}")
                self._abort_if_unique_id_configured()

                return self.async_create_entry(title="Edenic", data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=CONFIG_SCHEMA, errors=errors
        )


class OptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Edenic."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        errors: dict[str, str] = {}
        if user_input is not None:
            if not len(errors):
                new_data = self.config_entry.data.copy()

                self.hass.config_entries.async_update_entry(
                    self.config_entry,
                    data=new_data,
                )

                coordinator: EdenicDataUpdateCoordinator = self.hass.data[DOMAIN][
                    self.config_entry.entry_id
                ]

                return self.async_create_entry(title="", data={})

