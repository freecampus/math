"""Runtime settings for optional FreeCampus Math integrations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, cast

DEFAULT_OPENAI_MODEL: Final[str] = "gpt-5.4-mini"


@dataclass(frozen=True)
class FCMathSettings:
    """Configuration values used by optional FreeCampus Math integrations."""

    openai_api_key: str | None = None
    openai_model: str = DEFAULT_OPENAI_MODEL


_SETTINGS = FCMathSettings()
_UNSET: Final = object()


def configure(
    *,
    openai_api_key: str | object | None = _UNSET,
    openai_model: str | object = _UNSET,
) -> FCMathSettings:
    """Set global FreeCampus Math runtime settings.

    The settings module intentionally does not read environment variables. Apps,
    lessons, or notebooks should call this function explicitly when they want to
    enable optional services such as AI tutor explanations. Omitted arguments
    keep their previous values; pass ``None`` to clear ``openai_api_key``.
    """

    global _SETTINGS
    new_api_key = (
        _SETTINGS.openai_api_key
        if openai_api_key is _UNSET
        else cast(str | None, openai_api_key)
    )
    new_model = (
        _SETTINGS.openai_model if openai_model is _UNSET else cast(str, openai_model)
    )
    _SETTINGS = FCMathSettings(
        openai_api_key=new_api_key,
        openai_model=new_model,
    )
    return _SETTINGS


def get_settings() -> FCMathSettings:
    """Return the current FreeCampus Math runtime settings."""

    return _SETTINGS


def reset_settings() -> FCMathSettings:
    """Reset runtime settings to the package defaults."""

    global _SETTINGS
    _SETTINGS = FCMathSettings()
    return _SETTINGS


__all__ = [
    "DEFAULT_OPENAI_MODEL",
    "FCMathSettings",
    "configure",
    "get_settings",
    "reset_settings",
]
