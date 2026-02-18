"""Fields: a list of FIT field descriptors read from a definition record."""

from __future__ import annotations

from struct import pack
from typing import Any

from fit.types import KNOWN as KNOWN_TYPES

__all__ = ["Fields"]


class Fields(list):  # type: ignore[type-arg]
    """An ordered list of :class:`~fit.types.Type` instances describing a message layout.

    Attributes:
        field_size: Number of bytes per field descriptor in a definition record (3).
    """

    field_size: int = 3

    def __init__(self, iterable: Any = None) -> None:
        super().__init__(iterable or [])

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}{super().__repr__()}>"

    @property
    def size(self) -> int:
        """Total byte length of all fields combined."""
        return sum(field.size for field in self)

    def read(self, data: bytes) -> None:
        """Parse field descriptors from the raw bytes of a definition record.

        Each 3-byte chunk encodes: field number, field size, and base type.

        Args:
            data: Raw bytes from the definition record's field section.
        """
        for offset in range(0, len(data), self.field_size):
            chunk = data[offset : offset + self.field_size]
            base_type = chunk[2] & 0b00011111
            number = chunk[0]
            size = chunk[1]
            field = KNOWN_TYPES[base_type](number, size=size)
            self.append(field)

    def write(self) -> bytes:
        """Serialise the field list to bytes suitable for a definition record.

        Returns:
            3 bytes per field: ``(number, size, base_type_byte)``.
        """
        chunks = []
        for field in self:
            endian = int(field.size > 1)
            base_type = (endian << 7) | field.type
            chunks.append(pack("<BBB", field.number, field.size, base_type))
        return b"".join(chunks)
