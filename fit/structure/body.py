"""FIT file body: a sequence of FIT messages."""

from __future__ import annotations

from copy import copy
from io import BytesIO
from typing import Any

from fit.record.definition import Definition
from fit.record.fields import Fields
from fit.record.header import RecordHeader

__all__ = ["Body"]


class Body(list):  # type: ignore[type-arg]
    """An ordered list of FIT messages read from or to be written to a file."""

    def __init__(self, iterable: list | None = None) -> None:
        super().__init__(iterable or [])

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}[{len(self)}]>"

    def read(self, chunk: bytes) -> None:
        """Parse all records from *chunk* and append data messages to self.

        Definition records are processed for field layout but not stored.

        Args:
            chunk: Raw body bytes from the FIT file.
        """
        size = len(chunk)
        read_buffer = BytesIO(chunk)
        definitions: dict[int, Definition] = {}
        timestamp: int = 0
        offset: int = 0

        while read_buffer.tell() != size:
            header = RecordHeader.read(read_buffer.read(1)[0])
            message = header.process_message(definitions, read_buffer)
            timestamp, offset = message.process_timestamp(timestamp, offset)  # type: ignore[attr-defined]

            if not isinstance(message, Definition):
                self.append(message)

    def write(self) -> bytes:
        """Serialise all messages to bytes, de-duplicating definition records.

        Emits each unique definition record once (before the first data record
        of that type) and reuses the same local message index for subsequent
        data records.

        Returns:
            Packed bytes suitable for writing between the file header and CRC.
        """
        # Collect the union of fields used by each message type
        smallest: dict[int, set[Any]] = {}
        for item in self:
            number = item.definition.number
            current = smallest.get(number, set())
            smallest[number] = current | set(item.definition.fields)

        index = 0
        written: list[int] = []
        chunks: list[bytes] = []

        for item in self:
            number = item.definition.number

            try:
                local_index = written.index(number)
            except ValueError:
                local_index = index
                index += 1
                written.append(number)

                definition = copy(item.definition)
                definition.fields = Fields(smallest[number])
                chunks.append(definition.write(local_index))

            chunks.append(item.write(local_index, smallest[number]))

        return b"".join(chunks)
