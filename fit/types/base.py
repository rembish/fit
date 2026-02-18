"""Base type classes for the FIT binary type system."""

from __future__ import annotations

from struct import pack, unpack
from typing import IO, Any

from fit.utils import get_known

__all__ = ["KNOWN", "BinaryType", "Type"]


class Type:
    """Base class for all FIT data types.

    Each concrete subclass represents one of the FIT base types and knows
    how to read and write its binary representation.

    Attributes:
        type: FIT base type number (``None`` for abstract types).
        size: Default packed size in bytes.
        format: :mod:`struct` format character.
    """

    type: int | None = None
    size: int = 0
    format: str = "x"

    _invalid: Any = None

    def __init__(self, number: int, size: int | None = None) -> None:
        self.number = number
        self.size = size if size is not None else self.__class__.size

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Type):
            return NotImplemented
        return self.number == other.number

    def __hash__(self) -> int:
        return hash(self.number)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}[{self.number}]>"

    def read(self, read_buffer: IO[bytes], architecture: str = "<") -> Any:
        """Read and unpack one value from *read_buffer*.

        Args:
            read_buffer: Readable binary stream positioned at the field data.
            architecture: Struct byte-order prefix (``"<"`` or ``">"``).

        Returns:
            The unpacked Python value, or ``None`` if the value is the FIT
            invalid sentinel for this type.
        """
        data = unpack(
            f"{architecture}{self.format}",
            read_buffer.read(self.size),
        )[0]

        if data == self._invalid:
            return None

        return data

    def write(self, value: Any) -> bytes:
        """Pack *value* into bytes using little-endian byte order.

        Args:
            value: Python value to pack, or ``None`` (uses :attr:`_invalid`).

        Returns:
            Packed bytes of length :attr:`size`.
        """
        return pack(
            f"<{self.format}",
            value if value is not None else self._invalid,
        )

    def _load(self, data: Any) -> Any:
        """Convert raw binary value to a Python-friendly representation."""
        return data

    def _save(self, value: Any) -> Any:
        """Convert a Python value back to the raw binary representation."""
        return value


class BinaryType(Type):
    """A numeric FIT type that supports optional scale and offset conversions.

    Scale and offset follow the FIT convention: ``physical = raw / scale - offset``.

    The DSL operators allow inline declaration in message classes::

        speed = UInt16(6, units="m/s") * 1000    # scale of 1000
        altitude = UInt16(7, units="m") * 5 + 500 # scale 5, offset 500
    """

    def __init__(
        self,
        number: int,
        size: int | None = None,
        units: str | None = None,
    ) -> None:
        super().__init__(number, size=size)
        self.units: str | None = units
        self.scale: float | None = None
        self.offset: float | None = None

    def __mul__(self, other: Any) -> BinaryType:
        if isinstance(other, (int, float)):
            self.scale = float(other)
        if isinstance(other, str):
            self.units = other
        return self

    def __rmul__(self, other: Any) -> BinaryType:
        self.scale = float(other)
        return self

    def __sub__(self, other: Any) -> BinaryType:
        self.offset = float(-other)
        return self

    def __add__(self, other: Any) -> BinaryType:
        self.offset = float(other)
        return self

    def _load(self, data: Any) -> Any:
        if not self.scale and not self.offset:
            return super()._load(data)

        value = float(data)
        if self.scale:
            value /= self.scale
        if self.offset:
            value -= self.offset
        return value

    def _save(self, value: Any) -> Any:
        if not self.scale and not self.offset:
            return super()._save(value)

        data = float(value)
        if self.offset:
            data += self.offset
        if self.scale:
            data *= self.scale
        return int(data)


KNOWN: dict[Any, type] = get_known("fit.types", Type)
