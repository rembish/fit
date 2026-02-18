"""Composite field type: a field whose value is split across sub-components."""

from __future__ import annotations

from typing import IO, Any

from fit.types.base import Type

__all__ = ["ComponentField", "Composite"]


class Composite(Type):
    """A FIT field that wraps another type and exposes named bit-level components.

    The *base* type handles actual reading and writing; ``components`` describes
    the bit-field layout (currently informational).

    Args:
        base: Underlying :class:`~fit.types.Type` used for I/O.
        **kwargs: Named :class:`ComponentField` instances describing each component.
    """

    def __init__(self, base: Type, **kwargs: ComponentField) -> None:
        super().__init__(base.number)
        self.base: Type = base
        self.components = kwargs

    def read(self, read_buffer: IO[bytes], architecture: str = "<") -> Any:
        return self.base.read(read_buffer, architecture=architecture)

    def write(self, value: Any) -> bytes:
        return self.base.write(value)


class ComponentField:
    """Descriptor for a single bit-field component within a :class:`Composite` type.

    Args:
        bits: Number of bits this component occupies.
        offset: Bit offset within the composite value (default ``0``).
    """

    def __init__(self, bits: int, offset: int = 0) -> None:
        self.bits: int = bits
        self.offset: int = offset
        self.scale: float | None = None

    def __mul__(self, other: Any) -> ComponentField:
        self.scale = float(other)
        return self
