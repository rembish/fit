"""Composite field type: a field whose value is split across sub-components."""

from __future__ import annotations

from typing import IO, Any

from fit.types.base import Type

__all__ = ["ComponentField", "Composite"]


class Composite(Type):
    """A FIT field that wraps another type and exposes named bit-level components.

    The *base* type handles actual reading and writing; ``components`` describes
    the bit-field layout.

    Args:
        base: Underlying :class:`~fit.types.Type` used for I/O.
        **kwargs: Named :class:`ComponentField` instances describing each component.
    """

    def __init__(self, base: Type, **kwargs: ComponentField) -> None:
        super().__init__(base.number, size=base.size)
        self.base: Type = base
        self.components: dict[str, ComponentField] = kwargs

    def read(self, read_buffer: IO[bytes], architecture: str = "<") -> Any:
        return self.base.read(read_buffer, architecture=architecture)

    def write(self, value: Any) -> bytes:
        return self.base.write(value)

    def decompose(self, raw: Any) -> dict[str, Any]:
        """Extract all component values from *raw*.

        Args:
            raw: Raw bytes/list/int as stored in the message's ``_data``.

        Returns:
            Mapping of component name → physical value (scale applied).
        """
        return {name: field.extract(raw) for name, field in self.components.items()}


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

    def extract(self, raw: Any) -> Any:
        """Extract this component's value from *raw* bytes or integer.

        Args:
            raw: A list/bytes of byte values (little-endian) or an integer.

        Returns:
            The physical component value (scale divided out), or ``None`` if
            *raw* is ``None``.
        """
        if raw is None:
            return None
        if isinstance(raw, (list, tuple, bytes, bytearray)):
            raw_int = int.from_bytes(bytes(raw), byteorder="little")
        else:
            raw_int = int(raw)
        mask = (1 << self.bits) - 1
        component_raw = (raw_int >> self.offset) & mask
        if self.scale:
            return component_raw / self.scale
        return component_raw

    def pack_into(self, raw: Any, value: Any) -> Any:
        """Pack *value* into the component bits of *raw*.

        Args:
            raw: Existing raw bytes/list/int to merge into (``None`` means all zeros).
            value: Physical value to store (scale will be applied).

        Returns:
            Updated raw value in the same type as *raw* (list stays list,
            bytes stays bytes, int stays int).
        """
        component_raw = round(value * self.scale) if self.scale else int(value)
        mask = (1 << self.bits) - 1

        def _merge(raw_int: int) -> int:
            return (raw_int & ~(mask << self.offset)) | (
                (component_raw & mask) << self.offset
            )

        if isinstance(raw, (list, tuple)):
            length = len(raw)
            result = _merge(int.from_bytes(bytes(raw), byteorder="little"))
            return list(result.to_bytes(length, byteorder="little"))
        if isinstance(raw, (bytes, bytearray)):
            length = len(raw)
            result = _merge(int.from_bytes(raw, byteorder="little"))
            return result.to_bytes(length, byteorder="little")
        return _merge(int(raw) if raw is not None else 0)
