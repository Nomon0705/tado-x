"""Support for Tado Smart device trackers."""

from __future__ import annotations

import logging
from typing import cast

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
    """Set up Tado device tracker entities."""
    _LOGGER.debug("Setting up Tado device tracker entities")
    tado = entry.runtime_data
    tracked_devices: set[str] = set()

    # Temporary fix for non-string unique IDs (remove in 2025.1)
    entity_registry = er.async_get(hass)
    for device_key in tado.data["mobile_device"]:
        entity_id = entity_registry.async_get_entity_id(
            DEVICE_TRACKER_DOMAIN, DOMAIN, device_key
        )
        if entity_id:
            entity_registry.async_update_entity(
                entity_id, new_unique_id=str(device_key)
            )

    def update_devices() -> None:
        add_new_entities(hass, tado, async_add_entities, tracked_devices)

    update_devices()

    entry.async_on_unload(
        async_dispatcher_connect(
            hass,
            SIGNAL_TADO_MOBILE_DEVICE_UPDATE_RECEIVED.format(tado.home_id),
            update_devices,
        )
    )


@callback
def add_new_entities(
    hass: HomeAssistant,
    tado: TadoConnector,
    async_add_entities: AddEntitiesCallback,
    tracked: set[str],
) -> None:
    """Add new Tado mobile device tracker entities."""
    new_entities = []

    for device_key, device in tado.data["mobile_device"].items():
        if device_key in tracked:
            continue

        _LOGGER.debug("Adding Tado device %s (ID: %s)", device["name"], device_key)
        new_entities.append(
            TadoDeviceTrackerEntity(device_id=device_key, device=device, tado=tado)
        )
        tracked.add(device_key)

    async_add_entities(new_entities)


class TadoDeviceTrackerEntity(TrackerEntity):
    """Tado mobile device tracker entity."""

    _attr_should_poll = False
    _attr_available = False

    def __init__(
        self,
        device_id: str,
        device: dict,
        tado: TadoConnector,
    ) -> None:
        """Initialize the Tado tracker entity."""
        self._device_id = device_id
        self._device_name = device["name"]
        self._tado = tado
        self._active = False
        self._attr_unique_id = str(device_id)

    async def async_added_to_hass(self) -> None:
        """Register update callback when added to Home Assistant."""
        _LOGGER.debug("Registered Tado tracker: %s", self._device_name)

        self.async_on_remove(
            async_dispatcher_connect(
                self.hass,
                SIGNAL_TADO_MOBILE_DEVICE_UPDATE_RECEIVED.format(self._tado.home_id),
                self.on_demand_update,
            )
        )
        self.update_state()

    @callback
    def update_state(self) -> None:
        """Update the internal state from Tado data."""
        device = self._tado.data["mobile_device"][self._device_id]
        self._attr_available = False

        if device["settings"].get("geoTrackingEnabled"):
            self._attr_available = True
            self._active = device.get("location", {}).get("atHome", False)
            _LOGGER.debug(
                "Tado device %s is %s",
                device["name"],
                "at home" if self._active else "not at home",
            )
        else:
            _LOGGER.debug("Tado device %s has geoTracking disabled", device["name"])

    @callback
    def on_demand_update(self) -> None:
        """Trigger a state update."""
        self.update_state()
        self.async_write_ha_state()

    @property
    def name(self) -> str:
        return self._device_name

    @property
    def location_name(self) -> str:
        return STATE_HOME if self._active else STATE_NOT_HOME
