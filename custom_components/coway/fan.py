"""Support for Coway Air Purifiers."""

import logging
import voluptuous as vol
from homeassistant.helpers import config_validation as cv, entity_platform
from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.util.percentage import ordered_list_item_to_percentage
from homeassistant.components.fan import (
    FanEntity,
    SUPPORT_SET_SPEED,
    SUPPORT_PRESET_MODE,
)


"""Attributes"""

ATTR_NIGHT_MODE = "night_mode"
ATTR_AUTO_MODE = "auto_mode"
ATTR_PRE_FILTER_PERCENT = "pre_filter_percent"
ATTR_MAX2_FILTER_PERCENT = "max2_filter_percent"
ATTR_TIMER = "timer"
ATTR_TIMER_REMAINING = "timer_remaining"

SERVICE_SET_AUTO_MODE = "set_auto_mode_on"
SERVICE_SET_NIGHT_MODE = "set_night_mode_on"
SERVICE_SET_TIMER = "set_timer"

PRESET_MODE_AUTO = "Auto"
PRESET_MODE_NIGHT = "Night"


SET_AUTO_MODE_SCHEMA = {
    vol.Required(ATTR_ENTITY_ID): cv.entity_id,
}

SET_NIGHT_MODE_SCHEMA = {
    vol.Required(ATTR_ENTITY_ID): cv.entity_id,
}

SET_TIMER_SCHEMA = {
    vol.Required(ATTR_ENTITY_ID): cv.entity_id,
    vol.Required(ATTR_TIMER): cv.positive_int,
}

from .const import (
    DOMAIN,
    IOCARE_FAN_OFF,
    IOCARE_FAN_LOW,
    IOCARE_FAN_MEDIUM,
    IOCARE_FAN_HIGH,
    IOCARE_TIMER_OFF,
    IOCARE_TIMER_1H,
    IOCARE_TIMER_2H,
    IOCARE_TIMER_4H,
    IOCARE_TIMER_8H
)

ORDERED_NAMED_FAN_SPEEDS = [IOCARE_FAN_LOW, IOCARE_FAN_MEDIUM, IOCARE_FAN_HIGH]
PRESET_MODES = [PRESET_MODE_AUTO, PRESET_MODE_NIGHT]


IOCARE_FAN_SPEED_TO_HASS = {
    IOCARE_FAN_OFF: 0,
    IOCARE_FAN_LOW: ordered_list_item_to_percentage(ORDERED_NAMED_FAN_SPEEDS, IOCARE_FAN_LOW),
    IOCARE_FAN_MEDIUM: ordered_list_item_to_percentage(ORDERED_NAMED_FAN_SPEEDS, IOCARE_FAN_MEDIUM),
    IOCARE_FAN_HIGH: ordered_list_item_to_percentage(ORDERED_NAMED_FAN_SPEEDS, IOCARE_FAN_HIGH)
}

HASS_FAN_SPEED_TO_IOCARE = {v: k for (k, v) in IOCARE_FAN_SPEED_TO_HASS.items()}


_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Platform uses config entry setup."""
    pass


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Coway Air Purifier devices."""
    iocare = hass.data[DOMAIN]

    platform = entity_platform.current_platform.get()

    devices = []

    for device in iocare.devices():
        devices.append(AirPurifier(device))

    async_add_entities(devices)

    platform.async_register_entity_service(
        SERVICE_SET_AUTO_MODE,
        SET_AUTO_MODE_SCHEMA,
        "set_auto_mode_on",
    )

    platform.async_register_entity_service(
        SERVICE_SET_NIGHT_MODE,
        SET_NIGHT_MODE_SCHEMA,
        "set_night_mode_on",
    )

    platform.async_register_entity_service(
        SERVICE_SET_TIMER,
        SET_TIMER_SCHEMA,
        "set_timer",
    )

class AirPurifier(FanEntity):
    """Representation of a Coway Airmega air purifier."""

    def __init__(self, device):
        self._device = device
        self._available = True

    @property
    def device_info(self):
        """Return device registry information for this entity."""
        return {
            "identifiers": {(DOMAIN, self._device.device_id)},
            "name": self._device.name,
            "manufacturer": "Coway",
            "model": self._device.product_name_full,
        }

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
    def preset_modes(self):
        """Return the available preset modes"""
        return PRESET_MODES

    @property
    def preset_mode(self):
        """"Return the current preset mode"""
        if self._device.is_auto_eco:
            return PRESET_MODE_AUTO
        if self._device.is_auto:
            return PRESET_MODE_AUTO
        if self._device.is_night:
            return PRESET_MODE_NIGHT
        return None

    @property
    def auto_mode(self):
        """Return true if purifier speed is set to auto mode and false if off."""
        if self._device.is_auto_eco:
            return str(self._device.is_auto_eco).lower() + "(eco)"
        return self._device.is_auto

    @property
    def night_mode(self):
        """Return true if purifier speed is set to night mode and false if off."""
        return self._device.is_night

    @property
    def timer(self):
        """Return for how many hours timer is set to"""
        if (float(self._device.timer) / 60) == 0:
            return "off"
        return (float(self._device.timer) / 60)

    @property
    def timer_remaining(self):
        """Return hours left if a timer is on and 0 if no time left"""
        if round((float(self._device.timer_remaining) / 60), 2) == 0:
            return 0
        return round((float(self._device.timer_remaining) / 60), 2)

    @property
    def pre_filter_percent(self) -> int:
        """Return Pre-Filter Percentage"""
        return self._device.filters[0]["life_level_pct"]

    @property
    def max2_filter_percent(self) -> int:
        """Return MAX2 Filter Percentage"""
        return self._device.filters[1]["life_level_pct"]

    @property
    def available(self):
        """Return true if switch is available."""
        return self._available

    @property
    def percentage(self) -> int:
        """Return the current speed."""
        if not self._device.is_on:
            return 0
        return IOCARE_FAN_SPEED_TO_HASS.get(self._device.fan_speed)

    @property
    def speed_count(self) -> int:
        """Get the list of available speeds."""
        return len(ORDERED_NAMED_FAN_SPEEDS)

    @property
    def supported_features(self) -> int:
        """Flag supported features."""
        return SUPPORT_SET_SPEED | SUPPORT_PRESET_MODE

    @property
    def extra_state_attributes(self) -> dict:
        """Return optional state attributes."""
        return {
            ATTR_NIGHT_MODE: self.night_mode,
            ATTR_AUTO_MODE: self.auto_mode,
            ATTR_PRE_FILTER_PERCENT: self.pre_filter_percent,
            ATTR_MAX2_FILTER_PERCENT: self.max2_filter_percent,
            ATTR_TIMER: self.timer,
            ATTR_TIMER_REMAINING: self.timer_remaining,
        }

    def turn_on(self, percentage: int = None, **kwargs) -> None:
        """Turn the air purifier on."""
        self._device.set_power(True)
        if percentage is not None:
            self.set_percentage(percentage)

    def turn_off(self, **kwargs) -> None:
        """Turn the air purifier off."""
        self._device.set_power(False)

    def set_percentage(self, percentage: int) -> None:
        """Set the fan_mode of the air purifier."""
        if percentage == 0:
            return self.turn_off()
        if not self.is_on:
            self.turn_on()
            self._device.set_fan_speed(HASS_FAN_SPEED_TO_IOCARE.get(percentage))
        self._device.set_fan_speed(HASS_FAN_SPEED_TO_IOCARE.get(percentage))

    def set_preset_mode(self, preset_mode: str) -> None:
        """Set a preset mode on the fan."""
        if preset_mode == PRESET_MODE_AUTO:
            if not self._device.is_on:
                self.turn_on()
                self._device.set_auto_mode()
            self._device.set_auto_mode()
        if preset_mode == PRESET_MODE_NIGHT:
            if not self._device.is_on:
                self.turn_on()
                self._device.set_night_mode()
            self._device.set_night_mode()

    def set_auto_mode_on(self) -> None:
        """Sets Auto Mode to ON"""
        self._device.set_auto_mode()

    def set_night_mode_on(self) -> None:
        """Sets Night Mode to ON"""
        self._device.set_night_mode()

    def set_timer(self, timer) -> None:
        """Set timer."""
        while timer not in [0, 1, 2, 4, 8]:
            return _LOGGER.error("Only 0, 1, 2, 4, and 8 are accepted times")
        if timer == 0:
            self._device.set_timer(IOCARE_TIMER_OFF)
            self.timer_remaining
        if timer == 1:
            self._device.set_timer(IOCARE_TIMER_1H)
            self.timer_remaining
        if timer == 2:
            self._device.set_timer(IOCARE_TIMER_2H)
            self.timer_remaining
        if timer == 4:
            self._device.set_timer(IOCARE_TIMER_4H)
            self.timer_remaining
        if timer == 8:
            self._device.set_timer(IOCARE_TIMER_8H)
            self.timer_remaining

    def update(self):
        """Update automation state."""
        _LOGGER.info("Refreshing device state")
        self._device.refresh()
