# Coway IoCare Home Assistant Integration
<a href="https://www.buymeacoffee.com/RobertD502" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

**Donations aren't required, but are always appreciated. If you enjoy this integration, consider buying me a coffee by clicking on the logo above.**

Home Assistant custom component for monitoring and controlling Coway Airmega air purifiers.




## Installation

### With HACS
1. Open HACS Settings and add this repository (https://github.com/RobertD502/home-assistant-iocare)
as a Custom Repository (use **Integration** as the category).
2. The `Coway IoCare` page should automatically load (or find it in the HACS Store)
3. Click `Install`

### Manual
Copy the `coway` directory from `custom_components` in this repository,
and place inside your Home Assistant Core installation's `custom_components` directory.


## Setup
1. Install this integration.
2. Use Config Flow to configure the integration with your Coway IoCare credentials.
    * Initiate Config Flow by navigating to Configuration > Integrations > click the "+" button > find "Coway IoCare" (restart Home Assistant and / or clear browser cache if you can't find it)

# Devices

Each purifier is exposed as a device in Home Assistant.

Each purifier has the following entities:

| Entity | Entity Type | Additional Comments |
| --- | --- | --- |
| `Purifier` | `Fan` | Ability of controlling power, speed, and preset mode (Auto Mode, Night Mode) |
| `Current Timer` | `Select` | Ability to set timer to OFF, 1 hour, 2 hours, 4 hours, or 8 hours |
| `Purifier Light` | `Switch` | Ability to turn light on and off |
| `AQI` | `Sensor` | Air Quality Index |
| `Carbon Dioxide` | `Sensor` | |
| `MAX2 Filter` | `Sensor` | Percentage of MAX2 filter life remaining |
| `Pre Filter` | `Sensor` | Percentage of Pre filter remaining |
| `Particulate Matter 10` | `Sensor` | |
| `Particulate Matter 2.5` | `Sensor` | |
| `VOC` | `Sensor` | |
| `Timer Remaining` | `Sensor` | Shows the current amount of time left on a timer. This is a string in the form of hours:minutes |

