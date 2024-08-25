# Edenic Integration for Home Assistant
This custom component allows you to monitor and control your Bluelab devices in Home Assistant. The Edenic integration will create sensors for any devices configured in the Edenic app and automatically sync with the Edenic API for updates.

# Compatibility

This integration supports Bluelab monitors and controllers that are compaitble with the Edenic app. See [compatible devices from Bluelab](https://www.edenic.io/#hardware) for more information.

# Installation

## HACS

This integration is not yet available through the Home Assistant Community Store. Manually add this repository as a custom repository in HACS.

Please see the [official HACS documentation](https://hacs.xyz) for information on how to install and use HACS.

## Manual Installation

Copy `custom_components/edenic` into your Home Assistant `$HA_HOME/config` directory, then restart Home Assistant.

# Initial Setup

Add the Edenic integration from the integration section of the Home Assistant settings. You'll need to input the following credentials obtained from the [Edenic app](https://app.edenic.io/):

- `API Key`: The API key for your Edenic account.
- `Organization ID`: The organization ID for your Edenic account.

## Create an API key

1. Open the [Edenic app](https://app.edenic.io/) and sign in.
2. Click on your account avatar (in the top right) and navigate to Account settings > API Keys (you must be registered to see this).
3. Click Create new key and give your key a name (**note this key will expire in 1 year**).
4. Copy the API key or organization ID from here at anytime.

## Configuration Options

After adding the integration, the following options can be modified via the configuration options dialog:

- `Temperature Unit`: Choose between Celsius and Fahrenheit.
- `Conductivity Unit`: Choose between mS, µS, PPM 500, and PPM 700.
- `Scan Interval`: Set the interval for scanning devices, with a minimum value of 60 seconds due to rate limits with the Edenic API.

# Entities

## Sensors

Read-only sensors reported from the Edenic app:

- `Temperature`: The temperature as reported by the Bluelab probe in your controller.
- `pH`: The pH as reported by the Bluelab probe in your controller.
- `Electrical Conductivity`: The electrical conductivity as reported by the Bluelab probe in your controller.

### Binary Sensors (to-do)

Read-only alarms reported from the Edenic app:

- `pH High Alarm`: Triggered when the pH measurement is equal to or above the set pH High Alarm setting.
- `pH Low Alarm`: Triggered when the pH measurement is equal to or below the set pH Low Alarm setting.
- `Temperature High Alarm`: Triggered when the temperature measurement is equal to or above the set Temperature High Alarm setting.
- `Temperature Low Alarm`: Triggered when the temperature measurement is equal to or below the set Temperature Low Alarm setting.
- `EC High Alarm`: Triggered when the electrical conductivity measurement is equal to or above the set EC High Alarm setting.
- `EC Low Alarm`: Triggered when the electrical conductivity measurement is equal to or below the set EC Low Alarm setting.

### Numbers (to-do)

Editable settings for the controller:

- `Control Mode`: Choose between "MONITOR" or "CONTROL".
- `Required pH`: Set the required pH value (Range: 0.1 - 13.9).
- `pH Low Alarm`: Set the pH low alarm value (Range: 0.0 - 13.8).
- `pH High Alarm`: Set the pH high alarm value (Range: 0.2 - 14.0).
- `EC Low Alarm`: Set the EC low alarm value (Range: 0.0 - 4.8).
- `EC High Alarm`: Set the EC high alarm value (Range: 0.2 - 5.0).
- `Temperature Low Alarm`: Set the temperature low alarm value (Range: 0 - 47°C).
- `Temperature High Alarm`: Set the temperature high alarm value (Range: 3 - 50°C).

