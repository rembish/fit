"""Record header parsing: distinguishes definition, data, and compressed-timestamp records."""

from __future__ import annotations

from struct import pack
from typing import IO, TYPE_CHECKING

if TYPE_CHECKING:
    from fit.record.definition import Definition

__all__ = [
    "CompressedTimestampHeader",
    "DataHeader",
    "DefinitionHeader",
    "NormalHeader",
    "RecordHeader",
]


class RecordHeader:
    """Abstract base for FIT record headers.

    The first byte of every record encodes its type and the local message
    type number used to look up the matching definition.

    Args:
        local_message_type: 0-3 bit local message type index.
    """

    def __init__(self, local_message_type: int) -> None:
        self.type: int = local_message_type

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}[{self.type}]>"

    @classmethod
    def read(cls, byte: int) -> RecordHeader:
        """Parse one record-header byte and return the appropriate subclass.

        Args:
            byte: The raw header byte (0-255).

        Returns:
            A :class:`NormalHeader` or :class:`CompressedTimestampHeader`.
        """
        msg_type = (byte >> 7) & 1
        if msg_type:
            return CompressedTimestampHeader.read(byte)
        return NormalHeader.read(byte)

    def write(self) -> bytes:
        """Serialise the header to one byte."""
        raise NotImplementedError

    def process_message(
        self,
        definitions: dict[int, Definition],
        read_buffer: IO[bytes],
    ) -> object:
        """Read and return the message that follows this header."""
        raise NotImplementedError


class NormalHeader(RecordHeader):
    """A normal (non-compressed) record header."""

    msg_type: int | None = None

    @classmethod
    def read(cls, byte: int) -> NormalHeader:  # type: ignore[override]
        msg_type = (byte >> 6) & 1
        local_message_type = byte & 0b00001111
        if msg_type:
            return DefinitionHeader(local_message_type)
        return DataHeader(local_message_type)

    def write(self) -> bytes:
        assert self.msg_type is not None
        byte = 0 | (self.msg_type << 6) | self.type
        return pack("<B", byte)


class DefinitionHeader(NormalHeader):
    """Header for a definition record (msg_type bit = 1)."""

    msg_type = 1

    def process_message(
        self,
        definitions: dict[int, Definition],
        read_buffer: IO[bytes],
    ) -> object:
        from fit.record.definition import Definition

        return Definition.read(definitions, header=self, read_buffer=read_buffer)


class DataHeader(NormalHeader):
    """Header for a data record (msg_type bit = 0)."""

    msg_type = 0

    def process_message(
        self,
        definitions: dict[int, Definition],
        read_buffer: IO[bytes],
    ) -> object:
        definition = definitions[self.type]
        return definition.build_message(read_buffer)


class CompressedTimestampHeader(RecordHeader):
    """A compressed-timestamp record header (high bit = 1).

    These records implicitly carry a timestamp offset rather than a
    separate timestamp field, saving two bytes per record.

    Args:
        local_message_type: 2-bit local message type (bits 5-6).
        time_offset: 5-bit time offset from the previous full timestamp.
    """

    def __init__(self, local_message_type: int, time_offset: int) -> None:
        super().__init__(local_message_type)
        self.offset: int = time_offset

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}[{self.type}] {self.offset:+}>"

    @classmethod
    def read(cls, byte: int) -> CompressedTimestampHeader:  # type: ignore[override]
        local_message_type = (byte >> 5) & 0b11
        time_offset = byte & 0b00011111
        return cls(local_message_type, time_offset)

    def write(self) -> bytes:
        byte = 1 | (self.type << 5) | self.offset
        return pack("<B", byte)

    def process_message(
        self,
        definitions: dict[int, Definition],
        read_buffer: IO[bytes],
    ) -> object:
        definition = definitions[self.type]
        return definition.build_message(read_buffer)
