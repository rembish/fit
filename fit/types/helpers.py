"""Helpers and mixins for extended FIT types."""

from __future__ import annotations

from typing import Any

from fit.types.base import BinaryType
from fit.types.general import SInt32

__all__ = ["KnownMixin", "degrees"]


class KnownMixin:
    """Mixin that maps raw integer values to human-readable string names.

    Subclasses define a :attr:`known` dict of ``{raw_int: name_str}``.
    Values not in :attr:`known` are returned as-is (passthrough).
    """

    known: dict[int, str] = {}

    def _load(self, data: Any) -> Any:
        return self.known.get(data, data)

    def _save(self, value: Any) -> Any:
        for key, other in self.known.items():
            if value == other:
                return key
        return value


def degrees(number: int) -> BinaryType:
    """Return a :class:`~fit.types.general.SInt32` configured for semicircle → degrees conversion.

    FIT stores geographic coordinates in *semicircles*. This helper creates a
    field with the correct scale (2³¹ / 180) and unit label ``"°"``.

    Args:
        number: FIT field number.

    Returns:
        Configured :class:`~fit.types.general.SInt32` instance.
    """
    return SInt32(number, units="°") * (2**31 / 180.0)
