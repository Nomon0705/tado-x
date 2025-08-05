"""Support for Tado Smart device trackers."""

from __future__ import annotations

import logging

from homeassistant.components.device_tracker import (
    DOMAIN as DEVICE_TRACKER_DOMAIN,
    TrackerEntity,
)
from homeassistant.const import STATE_HOME, STATE_NOT_HOME
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import TadoConfigEntry
from .const import DOMAIN, SIGNAL_TADO_MOBILE_DEVICE_UPDATE_RECEIVED
from .tado_connector import TadoConnector

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: TadoConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Tado device scanner entities."""
    _LOGGER.debug("Setting up Tado device scanner entity")
    tado = entry.runtime_data
    tracked_devices: set[str] = set()

    # Fix non-string unique_id for device trackers (can be removed in 2025.1)
    entity_registry = er.async_get(hass)
    for device_key in tado.data["mobile_device"]:
        entity_id = entity_registry.async_get_entity_id(
            DEVICE_TRACKER_DOMAIN, DOMAIN, device_key
        )
        if entity_id:
            entity_registry.async_update_entity(entity_id, new_unique_id=str(device_key))

    def update_devices() -> None:
        """Update tracked devices."""
        add_tracked_entities(hass, tado, async_add_entities, tracked_devices)

    update_devices()

    # Register dispatcher for device updates
    entry.async_on_unload(
        async_dispatcher_connect(
            hass,
            SIGNAL_TADO_MOBILE_DEVICE_UPDATE_RECEIVED.format(tado.home_id),
            update_devices,
        )
    )


@callback
def add_tracked_entities(
    hass: HomeAssistant,
    tado: TadoConnector,
    async_add_entities: AddEntitiesCallback,
    tracked: set[str],
) -> None:
    """Add new Tado device tracker entities."""
    _LOGGER.debug("Fetching Tado devices for (newly) tracked entities")
    new_entities: list[TadoDeviceTrackerEntity] = []

    for device_key, device in tado.data["mobile_device"].items():
        if device_key in tracked:
            continue

        _LOGGER.debug(
            "Adding Tado device %s with deviceID %s", device["name"], device_key
        )
        new_entities.append(TadoDeviceTrackerEntity(device_key, device["name"], tado))
        tracked.add(device_key)

    async_add_entities(new_entities)


class TadoDeviceTrackerEntity(TrackerEntity):
    """A Tado Device Tracker entity."""

    _attr_should_poll = False
    _attr_available = False

    def __init__(
        self,
        device_id: str,
        device_name: str,
        tado: TadoConnector,
    ) -> None:
        """Initialize a Tado Device Tracker entity."""
        super().__init__()
        self._attr_unique_id = str(device_id)
        self._device_id = device_id
        self._device_name = device_name
        self._tado = tado
        self._active = False

    @callback
    def update_state(self) -> None:
        """Update the device's state."""
        device = self._tado.data["mobile_device"][self._device_id]

        # Reset availability; will set to True if geoTracking is enabled
        self._attr_available = False
        geo_tracking_enabled = device["settings"].get("geoTrackingEnabled", False)
        _LOGGER.debug(
            "Tado device %s geoTrackingEnabled: %s",
            device["name"],
            geo_tracking_enabled,
        )

        if not geo_tracking_enabled:
            return

        self._attr_available = True
        # Determine if device is at home
        location = device.get("location")
        if location and location.get("atHome"):
            _LOGGER.debug("Tado device %s is at home", device["name"])
            self._active = True
        else:
            _LOGGER.debug("Tado device %s is not at home", device["name"])
            self._active = False

    @callback
    def on_demand_update(self) -> None:
        """Handle on-demand state update."""
        self.update_state()
        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        """Register update callback on addition."""
        _LOGGER.debug("Registering Tado device tracker entity: %s", self._device_name)
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass,
                SIGNAL_TADO_MOBILE_DEVICE_UPDATE_RECEIVED.format(self._tado.home_id),
                self.on_demand_update,
            )
        )
        self.update_state()

    @property
    def name(self) -> str:
        """Return the device name."""
        return self._device_name

    @property
    def location_name(self) -> str:
        """Return the current location state."""
        return STATE_HOME if self._active else STATE_NOT_HOME