"""Runtime settings for optional edu-math integrations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, cast

DEFAULT_OPENAI_MODEL: Final[str] = "gpt-5.4-mini"


@dataclass(frozen=True)
class EduMathSettings:
    """Configuration values used by optional edu-math integrations."""

    openai_api_key: str | None = None
    openai_model: str = DEFAULT_OPENAI_MODEL


_SETTINGS = EduMathSettings()
_UNSET: Final = object()


def configure(
    *,
    openai_api_key: str | None | object = _UNSET,
    openai_model: str | object = _UNSET,
) -> EduMathSettings:
    """Set global edu-math runtime settings.

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
    _SETTINGS = EduMathSettings(
        openai_api_key=new_api_key,
        openai_model=new_model,
    )
    return _SETTINGS


def get_settings() -> EduMathSettings:
    """Return the current edu-math runtime settings."""

    return _SETTINGS


def reset_settings() -> EduMathSettings:
    """Reset runtime settings to the package defaults."""

    global _SETTINGS
    _SETTINGS = EduMathSettings()
    return _SETTINGS


__all__ = [
    "DEFAULT_OPENAI_MODEL",
    "EduMathSettings",
    "configure",
    "get_settings",
    "reset_settings",
]
