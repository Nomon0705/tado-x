"""Constant values for the Tado component."""

from PyTado.const import (
    CONST_HVAC_COOL,
    CONST_HVAC_DRY,
    CONST_HVAC_FAN,
    CONST_HVAC_HEAT,
    CONST_HVAC_HOT_WATER,
    CONST_HVAC_IDLE,
    CONST_HVAC_OFF,
)

from homeassistant.components.climate import (
    FAN_AUTO,
    FAN_HIGH,
    FAN_LOW,
    FAN_MEDIUM,
    FAN_OFF,
    PRESET_AWAY,
    PRESET_HOME,
    SWING_OFF,
    SWING_ON,
    HVACAction,
    HVACMode,
)

# HVAC Action mappings
TADO_HVAC_ACTION_TO_HA = {
    CONST_HVAC_HEAT: HVACAction.HEATING,
    CONST_HVAC_DRY: HVACAction.DRYING,
    CONST_HVAC_FAN: HVACAction.FAN,
    CONST_HVAC_COOL: HVACAction.COOLING,
    CONST_HVAC_IDLE: HVACAction.IDLE,
    CONST_HVAC_OFF: HVACAction.OFF,
    CONST_HVAC_HOT_WATER: HVACAction.HEATING,
}

# Configuration constants
CONF_FALLBACK = "fallback"
CONF_HOME_ID = "home_id"
DATA = "data"

# Weather condition to categories mapping
CONDITIONS_MAP = {
    "clear-night": {"NIGHT_CLEAR"},
    "cloudy": {"CLOUDY", "CLOUDY_MOSTLY", "NIGHT_CLOUDY"},
    "fog": {"FOGGY"},
    "hail": {"HAIL", "RAIN_HAIL"},
    "lightning": {"THUNDERSTORM"},
    "partlycloudy": {"CLOUDY_PARTLY"},
    "rainy": {"DRIZZLE", "RAIN", "SCATTERED_RAIN"},
    "snowy": {"FREEZING", "SCATTERED_SNOW", "SNOW"},
    "snowy-rainy": {"RAIN_SNOW", "SCATTERED_RAIN_SNOW"},
    "sunny": {"SUN"},
    "windy": {"WIND"},
}

# Types
class Types:
    AIR_CONDITIONING = "AIR_CONDITIONING"
    HEATING = "HEATING"
    HOT_WATER = "HOT_WATER"
    BATTERY = "BATTERY"
    POWER = "POWER"

# Modes
class Modes:
    OFF = "OFF"
    SMART_SCHEDULE = "SMART_SCHEDULE"
    AUTO = "AUTO"
    COOL = "COOL"
    HEAT = "HEAT"
    DRY = "DRY"
    FAN = "FAN"

# Overlay modes
OVERLAY_MODES = {
    "NEXT_TIME_BLOCK": "NEXT_TIME_BLOCK",
    "MANUAL": "MANUAL",
    "TADO_DEFAULT": "TADO_DEFAULT",
}
OVERLAY_MODE_LIST = list(OVERLAY_MODES.values())

# Overlay group
OVERLAY_GROUP = "overlay_group"

# Known modes order (priority)
ORDERED_KNOWN_TADO_MODES = [
    Modes.HEAT,
    Modes.COOL,
    Modes.AUTO,
    Modes.DRY,
    Modes.FAN,
]

# Tado modes to HA HVAC actions
TADO_MODE_TO_HA_ACTION = {
    Modes.HEAT: HVACAction.HEATING,
    Modes.DRY: HVACAction.DRYING,
    Modes.FAN: HVACAction.FAN,
    Modes.COOL: HVACAction.COOLING,
}

# Modes where temperature cannot be set
TADO_MODES_WITH_NO_TEMP = [Modes.AUTO, Modes.FAN]

# Mapping between HA and Tado modes
HA_TO_TADO_HVAC_MODE = {
    HVACMode.OFF: Modes.OFF,
    HVACMode.HEAT_COOL: Modes.AUTO,
    HVACMode.AUTO: Modes.SMART_SCHEDULE,
    HVACMode.HEAT: Modes.HEAT,
    HVACMode.COOL: Modes.COOL,
    HVACMode.DRY: Modes.DRY,
    HVACMode.FAN_ONLY: Modes.FAN,
}

# Legacy fan mode mappings
FAN_MODE_LEGACY_MAP = {
    FAN_AUTO: Modes.AUTO,
    FAN_OFF: Modes.OFF,
    FAN_LOW: "LOW",
    FAN_MEDIUM: "MIDDLE",
    FAN_HIGH: "HIGH",
}

# Current fan mode mappings
FAN_MODE_MAP = {
    FAN_AUTO: "LEVEL1",
    FAN_OFF: "LEVEL0",
    FAN_LOW: "LEVEL1",
    FAN_MEDIUM: "LEVEL2",
    FAN_HIGH: "LEVEL3",
}

# Reverse mappings
def invert_dict(d):
    return {v: k for k, v in d.items()}

TADO_TO_HA_HVAC_MODE = invert_dict(HA_TO_TADO_HVAC_MODE)
TADO_TO_HA_FAN_MODE_LEGACY = invert_dict(FAN_MODE_LEGACY_MAP)
TADO_TO_HA_FAN_MODE = invert_dict(FAN_MODE_MAP)

# Fan speeds and levels
TADO_FAN_SPEEDS = list(FAN_MODE_LEGACY_MAP.values())
TADO_FAN_LEVELS = list(FAN_MODE_MAP.values())

# Default precision
DEFAULT_TADO_PRECISION = 0.1

# Presets
PRESET_AUTO = "auto"
SUPPORT_PRESET_AUTO = [PRESET_AWAY, PRESET_HOME, PRESET_AUTO]
SUPPORT_PRESET_MANUAL = [PRESET_AWAY, PRESET_HOME]

# Sensor categories
SENSOR_DATA_CATEGORY = {
    "WEATHER": "weather",
    "GEOFENCE": "geofence",
}

# Swing modes
SWING_OFF = "OFF"
SWING_ON = "ON"

# Swing mode mappings
SWING_MODE_MAP = {
    SWING_OFF: "OFF",
    SWING_ON: "ON",
}
REVERSE_SWING_MODE_MAP = invert_dict(SWING_MODE_MAP)

# Domain and signals
DOMAIN = "tado"
SIGNAL_UPDATE_RECEIVED = "tado_update_received_{}_{}_{}"
SIGNAL_MOBILE_UPDATE_RECEIVED = "tado_mobile_device_update_received_{}"
UNIQUE_ID = "unique_id"
DEFAULT_NAME = "Tado"

# Home and zone
HOME = "Home"
ZONE = "Zone"

# Temperature offset constants
class TemperatureOffset:
    MEASUREMENT = "INSIDE_TEMPERATURE_MEASUREMENT"
    OFFSET = "temperatureOffset"
    TADO_CELSIUS = "celsius"
    HA_CELSIUS = "offset_celsius"
    TADO_FAHRENHEIT = "fahrenheit"
    HA_FAHRENHEIT = "offset_fahrenheit"
    OFFSET_MAP = {
        TADO_CELSIUS: HA_CELSIUS,
        TADO_FAHRENHEIT: HA_FAHRENHEIT,
    }

# Overlay default settings
class OverlayDefaults:
    TERMINATION_TYPE = "default_overlay_type"
    TERMINATION_DURATION = "default_overlay_seconds"
    MIN_TEMP = 5
    MAX_TEMP = 40
    X_MIN_TEMP = 5
    X_MAX_TEMP = 30

# Service constants
SERVICE_ADD_METER_READING = "add_meter_reading"
CONF_CONFIG_ENTRY = "config_entry"
CONF_READING = "reading"
ATTR_MESSAGE = "message"

# Water heater fallback
WATER_HEATER_FALLBACK_REPAIR = "water_heater_fallback"

# Tado settings
TADO_SETTINGS = {
    "SWINGS": "swings",
    "FAN_SPEEDS": "fanSpeeds",
    "FAN_LEVEL": "fanLevel",
    "VERTICAL_SWING": "verticalSwing",
    "HORIZONTAL_SWING": "horizontalSwing",
    "LINE_X": "is_x",
    "PRE_LINE_X": "is_pre_x",
}