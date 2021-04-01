# Coway IoCare
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs) ![LGTM Grade](https://img.shields.io/lgtm/grade/python/github/sarahhenkens/home-assistant-iocare) ![GitHub manifest version (path)](https://img.shields.io/github/manifest-json/v/sarahhenkens/home-assistant-iocare?filename=custom_components%2Fcoway%2Fmanifest.json) ![GitHub all releases](https://img.shields.io/github/downloads/sarahhenkens/home-assistant-iocare/total?color=green)

Custom component for Home Assistant Core for monitoring and controlling
Coway / Airmega air purifiers.

**Breaking Change 0.0.1**

The recent update of home-assistant-iocare to `0.0.1` uses a new domain. If you previously installed any version prior to `0.0.1`, you will need to delete the integration from the integrations page in Home Assistant. Due to the new domain name, previous integrations will fail to work.
1. Delete your current IOCare Integration from the Home Assistant Integrations page
   1. If you updated prior to deleting the integration, delete the integration, restart Home Assistant, and proceed to step 4
2. Update home-assistant-iocare via HACS or manually
3. Restart Home Assistant
4. Initiate Config Flow by navigating to Configuration > Integrations > click the "+" button > find "Coway IoCare"
5. Enter your Coway IoCare credentials

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
