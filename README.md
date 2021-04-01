# Coway IoCare
Custom component for Home Assistant Core for monitoring and controlling
Coway / Airmega air purifiers.


## Installation

### With HACS
1. Open HACS Settings and add this repository (https://github.com/sarahhenkens/home-assistant-iocare)
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
