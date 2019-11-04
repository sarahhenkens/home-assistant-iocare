"""Support for Coway Air Purifiers."""

import logging

from homeassistant.components.fan import FanEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Platform uses config entry setup."""
    pass


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Abode switch devices."""
    _LOGGER.info("Setting up config entry for the FAN platform")

    iocare = hass.data[DOMAIN]

    devices = []

    for device in iocare.devices():
        _LOGGER.info("Creating a device instance with barcode: %s" % (device.device_id))
        devices.append(AirPurifier(device))

    async_add_entities(devices)


class AirPurifier(FanEntity):
    """Representation of a Coway Airmega air purifier."""

    def __init__(self, device):
        self._device = device
        self._available = True

    @property
    def unique_id(self):
        """Return the ID of this purifier."""
        return self._device.device_id

    @property
    def name(self):
        """Return the name of the purifier if any."""
        return self._device.name

    @property
    def is_on(self):
        """Return true if the purifier is on"""
        return self._device.is_on

    @property
    def available(self):
        """Return true if switch is available."""
        return self._available

    def turn_on(self, speed: str = None, **kwargs) -> None:
        """Turn the air purifier on."""
        self._device.set_power(True)

    def turn_off(self, **kwargs) -> None:
        """Turn the air purifier off."""
        self._device.set_power(False)

    def update(self):
        """Update automation state."""
        _LOGGER.info("Refreshing device state")
        self._device.refresh()

