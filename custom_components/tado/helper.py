"""Helper methods for Tado."""

from .const import (
    CONST_OVERLAY_TADO_DEFAULT,
    CONST_OVERLAY_TADO_MODE,
    CONST_OVERLAY_TIMER,
)
from .tado_connector import TadoConnector


def decide_overlay_mode(
    tado: TadoConnector,
    duration: int | None,
    zone_id: int,
    overlay_mode: str | None = None,
) -> str:
    """Return correct overlay mode based on the action and defaults."""
    # If user gave duration then overlay mode needs to be timer
    if duration:
        return CONST_OVERLAY_TIMER
    # If no duration or timer set to fallback setting
    if overlay_mode is None:
        overlay_mode = tado.fallback or CONST_OVERLAY_TADO_MODE
    # If default is Tado default then look it up
    if overlay_mode == CONST_OVERLAY_TADO_DEFAULT:
        overlay_mode = (
            tado.data["zone"][zone_id].default_overlay_termination_type
            or CONST_OVERLAY_TADO_MODE
        )

    return overlay_mode


# def decide_duration(
#     tado: TadoConnector,
#     duration: int | None,
#     zone_id: int,
#     overlay_mode: str | None = None,
# ) -> None | int:
#     """Return correct duration based on the selected overlay mode/duration and tado config."""
#     # If we ended up with a timer but no duration, set a default duration
#     # If we ended up with a timer but no duration, set a default duration
#     if overlay_mode == CONST_OVERLAY_TIMER and duration is None:
#         duration = (
#             int(tado.data["zone"][zone_id].default_overlay_termination_duration)
#             if tado.data["zone"][zone_id].default_overlay_termination_duration
#             is not None
#             else 3600
#         )

#     return duration



#     """Return correct list of fan modes or None."""
#     supported_fanmodes = [
#         tado_to_ha_mapping.get(option)
#         for option in options
#         if tado_to_ha_mapping.get(option) is not None
#     ]
#     if not supported_fanmodes:
#         return None
#     return supported_fanmodes



# """Helper methods for Tado."""

# from typing import Optional, List, Dict

# from .const import (
#     CONST_OVERLAY_TADO_DEFAULT,
#     CONST_OVERLAY_TADO_MODE,
#     CONST_OVERLAY_TIMER,
# )


# def decide_overlay_mode(
#     tado: TadoConnector,
#     duration: Optional[int],
#     zone_id: int,
#     overlay_mode: Optional[str] = None,
# ) -> str:
#     """Determine the correct overlay mode based on input and defaults."""
#     # Use timer if duration is specified
#     if duration:
#         return CONST_OVERLAY_TIMER

#     # Use provided overlay_mode or fallback to default

#         overlay_mode = tado.fallback or CONST_OVERLAY_TADO_MODE

#     # If overlay_mode is default, look up zone-specific setting
#     if overlay_mode == CONST_OVERLAY_TADO_DEFAULT:
#         zone_data = tado.data["zone"].get(zone_id, {})
#         default_overlay = zone_data.get("default_overlay_termination_type")
#         overlay_mode = default_overlay or CONST_OVERLAY_TADO_MODE

#     return overlay_mode


# def decide_duration(
#     tado: TadoConnector,
#     duration: Optional[int],
#     zone_id: int,
#     overlay_mode: Optional[str] = None,
# ) -> Optional[int]:
#     """Determine the correct duration based on overlay mode and tado config."""
#     if overlay_mode == CONST_OVERLAY_TIMER and duration is None:
#         zone_data = tado.data["zone"].get(zone_id, {})
#         default_duration = zone_data.get("default_overlay_termination_duration")
#         if default_duration is not None:
#             try:
#                 duration = int(default_duration)
#             except (TypeError, ValueError):
#                 duration = 3600
#         else:
#             duration = 3600
#     return duration


# def generate_supported_fanmodes(
#     tado_to_ha_mapping: Dict[str, str],
#     options: List[str]
# ) -> Optional[List[str]]:
#     """Return list of supported fan modes or None if none supported."""
#     supported_fanmodes = [
#         tado_to_ha_mapping.get(option)
#         for option in options
#         if tado_to_ha_mapping.get(option) is not None
#     ]
#     return supported_fanmodes if supported_fanmodes else None