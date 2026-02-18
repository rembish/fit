"""Definition record: the FIT message schema sent before data records."""

from __future__ import annotations

from copy import copy
from struct import pack, unpack
from typing import IO

from fit.messages import KNOWN as KNOWN_MESSAGES
from fit.messages.generic import GenericMessage
from fit.record.fields import Fields

__all__ = ["Definition"]


class Definition:
    """Schema descriptor for one local message type.

    A definition record is emitted by the encoder before the first data
    record of each message type and declares which fields (and their byte
    sizes) follow in the data records.

    Attributes:
        LITTLE: Byte-order constant for little-endian (0).
        BIG: Byte-order constant for big-endian (1).
        header: The :class:`~fit.record.header.RecordHeader` that introduced this definition.
        byte_order: ``LITTLE`` or ``BIG``.
        number: Global FIT message number.
        fields: Ordered list of field descriptors.
    """

    LITTLE: int = 0
    BIG: int = 1

    def __init__(self, header: object) -> None:
        self.header = header
        self.byte_order: int = self.BIG
        self.number: int | None = None
        self.fields: Fields = Fields()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}[{self.number}] with {self.fields!r}>"

    @property
    def architecture(self) -> str:
        """Struct byte-order prefix: ``"<"`` (little) or ``">"`` (big)."""
        return {self.LITTLE: "<", self.BIG: ">"}.get(self.byte_order, "<")

    @classmethod
    def read(
        cls,
        definitions: dict[int, Definition],
        header: object,
        read_buffer: IO[bytes],
    ) -> Definition:
        """Parse a definition record from *read_buffer* and register it.

        Args:
            definitions: Mutable dict mapping local message type → Definition.
            header: The record header that preceded this definition.
            read_buffer: Readable binary stream positioned after the header.

        Returns:
            The newly parsed :class:`Definition`.
        """
        instance = cls(header)
        _, instance.byte_order = unpack("<BB", read_buffer.read(2))
        instance.number, fields_count = unpack(
            f"{instance.architecture}HB",
            read_buffer.read(3),
        )

        chunk = read_buffer.read(fields_count * Fields.field_size)
        instance.fields.read(chunk)

        definitions[instance.header.type] = instance  # type: ignore[attr-defined]
        return instance

    def write(self, index: int) -> bytes:
        """Serialise this definition to bytes.

        Args:
            index: Local message type index (0-15) assigned by the encoder.

        Returns:
            Packed definition bytes: header + reserved + fields.
        """
        from fit.record.header import DefinitionHeader

        chunk = pack("<BBHB", 0, self.LITTLE, self.number, len(self.fields))
        return DefinitionHeader(index).write() + chunk + self.fields.write()

    def build_message(self, read_buffer: IO[bytes]) -> object:
        """Instantiate and populate the matching message class from *read_buffer*.

        Args:
            read_buffer: Readable binary stream positioned at the data fields.

        Returns:
            A populated :class:`~fit.messages.Message` instance (or
            :class:`~fit.messages.generic.GenericMessage` for unknown types).
        """
        message_cls = KNOWN_MESSAGES.get(self.number, GenericMessage)
        message = message_cls(copy(self))
        if isinstance(message, GenericMessage):
            message.msg_type = self.number

        message.read(read_buffer, copy(self.fields))
        return message

    def process_timestamp(self, timestamp: int, offset: int) -> tuple[int, int]:
        """Pass-through: definition records carry no timestamp."""
        return timestamp, offset
