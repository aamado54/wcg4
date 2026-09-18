"""Escenarios de stress test gerencial."""

from .nov2026 import (
    BASE_PRESETS,
    DRIVER_FIELDS,
    PRESETS,
    VIVO_PRESETS,
    build_nov2026_board,
    default_shocks,
    parse_shock,
)
from .precauciones import PRECAUTION_ARTICLES, get_precaution_article

__all__ = [
    "BASE_PRESETS",
    "DRIVER_FIELDS",
    "PRESETS",
    "VIVO_PRESETS",
    "build_nov2026_board",
    "default_shocks",
    "parse_shock",
    "PRECAUTION_ARTICLES",
    "get_precaution_article",
]
