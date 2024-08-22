# homeassistant-edenic

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

[![codecov](https://codecov.io/gh/taliexo/homeassistant-edenic/graph/badge.svg?token=C4TMDAU344)](https://codecov.io/gh/taliexo/homeassistant-edenic)
[![Tests](https://github.com/taliexo/homeassistant-edenic/actions/workflows/tests.yaml/badge.svg)](https://github.com/taliexo/homeassistant-edenic/actions/workflows/tests.yaml)

[![HACS/HASS](https://github.com/taliexo/homeassistant-edenic/actions/workflows/validate.yaml/badge.svg)](https://github.com/taliexo/homeassistant-edenic/actions/workflows/validate.yaml)
[![Code Style](https://github.com/taliexo/homeassistant-edenic/actions/workflows/style.yaml/badge.svg)](https://github.com/taliexo/homeassistant-edenic/actions/workflows/style.yaml)
[![CodeQL](https://github.com/taliexo/homeassistant-edenic/actions/workflows/codeql.yaml/badge.svg)](https://github.com/taliexo/homeassistant-edenic/actions/workflows/codeql.yaml)

This is a custom component for [Home Assistant](http://home-assistant.io) that adds support for [Edenic](https://endenic.io/) Bluelab devices within the [Endenic app](https://app.edenic.io/) cloud ecosystem.

- [Compatibility](#compatibility)
- [Installation](#installation)
  - [HACS](#hacs)
  - [Manual Installation](#manual-installation)
- [Initial Setup](#initial-setup)
  - [Additional Configuration](#additional-configuration)
- [Entities](#entities)
  - [Sensors](#sensors)

# Compatibility

This integration requires the controller be connected to Wifi, and thus is not compatible with bluetooth only devices.

# Installation

## HACS

This integration is made available through the Home Assistant Community Store default feed. Simply search for "Edenic" and install it directly from HACS.

![HACS-Instal](/images/hacs-install.png)

Please see the [official HACS documentation](https://hacs.xyz) for information on how to install and use HACS.

## Manual Installation

Copy `custom_components/edenic` into your Home Assistant `$HA_HOME/config` directory, then restart Home Assistant

# Initial Setup
Add an integration entry as normal from integration section of the home assistant settings. You'll need the following configuration items

- `API Key`: The API key for your Edenic account.
- `Organization ID`: The organization ID for your Edenic account.

![Initial-Setup](/images/initial-setup.png)

## Additional Configuration

After adding an integration entry, the following additional configurations can be modified via the configuration options dialog.

- `Update API Key`: When provided, updates the API key used to connect to your Edenic account. Requires Home Assistant restart.

![Additional-Configuration](/images/additional-configuration.png)

## Sensors
Read Only sensors reported from the controller
- `Temperature`: The temperature as reported by the Bluelab probe.
- `pH`: The pH as reported by the Bluelab probe.
- `Electrical Conductivity`: The electrical conductivity as reported by the Bluelab probe.
