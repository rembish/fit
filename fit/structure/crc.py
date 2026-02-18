"""CRC-16 checksum implementation for the FIT file format."""

from __future__ import annotations

from struct import Struct

__all__ = ["Crc", "compute_crc"]

_CRC_TABLE = [
    0x0000,
    0xCC01,
    0xD801,
    0x1400,
    0xF001,
    0x3C00,
    0x2800,
    0xE401,
    0xA001,
    0x6C00,
    0x7800,
    0xB401,
    0x5000,
    0x9C01,
    0x8801,
    0x4400,
]


def _process_byte(crc: int, byte: int) -> int:
    """Update a running CRC-16 value with a single byte."""
    temp = _CRC_TABLE[crc & 0xF]
    crc = (crc >> 4) & 0x0FFF
    crc = crc ^ temp ^ _CRC_TABLE[byte & 0xF]

    temp = _CRC_TABLE[crc & 0xF]
    crc = (crc >> 4) & 0x0FFF
    crc = crc ^ temp ^ _CRC_TABLE[(byte >> 4) & 0xF]

    return crc


def compute_crc(chunk: bytes) -> int:
    """Compute the CRC-16 checksum over *chunk*.

    Args:
        chunk: Raw bytes to checksum.

    Returns:
        16-bit CRC value.
    """
    crc = 0
    for byte in chunk:
        crc = _process_byte(crc, byte)
    return crc


class Crc:
    """Two-byte CRC-16 field at the end of a FIT file or header.

    Attributes:
        size: Packed size in bytes (always 2).
        value: The CRC value, or ``None`` if not yet read/computed.
    """

    def __init__(self) -> None:
        self._format: Struct = Struct("<H")
        self.size: int = self._format.size
        self.value: int | None = None

    def __bool__(self) -> bool:
        return self.value is not None

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} "{self.value or "-"}">'

    def read(self, chunk: bytes) -> None:
        """Unpack and store the CRC value from *chunk*."""
        self.value = self._format.unpack(chunk)[0]

    def write(self) -> bytes:
        """Pack the CRC value (zero if not set) into bytes."""
        return self._format.pack(self.value or 0)

    def check(self, chunk: bytes) -> bool:
        """Return ``True`` if :func:`compute_crc` of *chunk* matches :attr:`value`."""
        return compute_crc(chunk) == self.value
