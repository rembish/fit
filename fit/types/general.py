"""Core FIT base types: integers, floats, strings, enumerations, and bytes."""

from __future__ import annotations

from typing import Any

from fit.types.base import BinaryType, Type

__all__ = [
    "Byte",
    "Enum",
    "Float32",
    "Float64",
    "SInt8",
    "SInt16",
    "SInt32",
    "String",
    "UInt8",
    "UInt8Z",
    "UInt16",
    "UInt16Z",
    "UInt32",
    "UInt32Z",
]


class Enum(Type):
    """One-byte enumeration type.

    Subclasses provide a :attr:`variants` mapping of ``{raw_int: str_name}``.
    """

    type = 0
    size = 1
    format = "B"
    variants: dict[int, str] = {}

    _invalid = 0xFF

    def _load(self, data: Any) -> Any:
        return self.variants.get(data, data)

    def _save(self, value: Any) -> Any:
        for key, other in self.variants.items():
            if value == other:
                return key
        return value


class SInt8(BinaryType):
    """Signed 8-bit integer (FIT base type 1)."""

    type = 1
    size = 1
    format = "b"
    _invalid = 0x7F


class UInt8(BinaryType):
    """Unsigned 8-bit integer (FIT base type 2)."""

    type = 2
    size = 1
    format = "B"
    _invalid = 0xFF


class SInt16(BinaryType):
    """Signed 16-bit integer (FIT base type 3)."""

    type = 3
    size = 2
    format = "h"
    _invalid = 0x7FFF


class UInt16(BinaryType):
    """Unsigned 16-bit integer (FIT base type 4)."""

    type = 4
    size = 2
    format = "H"
    _invalid = 0xFFFF


class SInt32(BinaryType):
    """Signed 32-bit integer (FIT base type 5)."""

    type = 5
    size = 4
    format = "i"
    _invalid = 0x7FFFFFFF


class UInt32(BinaryType):
    """Unsigned 32-bit integer (FIT base type 6)."""

    type = 6
    size = 4
    format = "I"
    _invalid = 0xFFFFFFFF


class String(Type):
    """Null-terminated UTF-8 string (FIT base type 7).

    The *size* parameter controls how many bytes are read/written.
    """

    type = 7
    size = 1
    _invalid = 0x00

    def __init__(self, number: int, size: int | None = None) -> None:
        super().__init__(number, size=size)

    @property  # type: ignore[override]
    def format(self) -> str:  # type: ignore[override]
        return f"{self.size}s"


class Float32(Type):
    """IEEE-754 single-precision float (FIT base type 8)."""

    type = 8
    size = 4
    format = "f"
    _invalid = 0xFFFFFFFF


class Float64(Type):
    """IEEE-754 double-precision float (FIT base type 9)."""

    type = 9
    size = 8
    format = "d"
    _invalid = 0xFFFFFFFFFFFFFFFF


class UInt8Z(Type):
    """Unsigned 8-bit integer with zero as the invalid sentinel (FIT base type 10)."""

    type = 10
    size = 1
    format = "B"
    _invalid = 0x00


class UInt16Z(Type):
    """Unsigned 16-bit integer with zero as the invalid sentinel (FIT base type 11)."""

    type = 11
    size = 2
    format = "H"
    _invalid = 0x0000


class UInt32Z(Type):
    """Unsigned 32-bit integer with zero as the invalid sentinel (FIT base type 12)."""

    type = 12
    size = 4
    format = "I"
    _invalid = 0x00000000


class Byte(Type):
    """Raw byte (FIT base type 13)."""

    type = 13
    size = 1
    format = "c"
    _invalid = 0xFF
