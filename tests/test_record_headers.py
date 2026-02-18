"""Tests for fit.record.header — focusing on CompressedTimestampHeader."""

from __future__ import annotations

import struct
from io import BytesIO

import pytest

from fit.messages.common import FileCreator
from fit.record.definition import Definition
from fit.record.fields import Fields
from fit.record.header import (
    CompressedTimestampHeader,
    DataHeader,
    DefinitionHeader,
    RecordHeader,
)
from fit.types.general import UInt16

# ---------------------------------------------------------------------------
# RecordHeader dispatch
# ---------------------------------------------------------------------------


def test_record_header_read_dispatches_to_data() -> None:
    # bit 7 = 0, bit 6 = 0 → DataHeader, local type 0
    h = RecordHeader.read(0b00000000)
    assert isinstance(h, DataHeader)
    assert h.type == 0


def test_record_header_read_dispatches_to_definition() -> None:
    # bit 7 = 0, bit 6 = 1 → DefinitionHeader
    h = RecordHeader.read(0b01000000)
    assert isinstance(h, DefinitionHeader)


def test_record_header_read_dispatches_to_compressed_timestamp() -> None:
    # bit 7 = 1 → CompressedTimestampHeader
    h = RecordHeader.read(0b10000000)
    assert isinstance(h, CompressedTimestampHeader)


def test_record_header_repr() -> None:
    h = RecordHeader(3)
    assert "RecordHeader" in repr(h)
    assert "3" in repr(h)


def test_record_header_write_raises_not_implemented() -> None:
    with pytest.raises(NotImplementedError):
        RecordHeader(0).write()


def test_record_header_process_message_raises_not_implemented() -> None:
    with pytest.raises(NotImplementedError):
        RecordHeader(0).process_message({}, BytesIO(b""))


# ---------------------------------------------------------------------------
# CompressedTimestampHeader: construction and repr
# ---------------------------------------------------------------------------


def test_compressed_ts_header_type_and_offset() -> None:
    h = CompressedTimestampHeader(2, 17)
    assert h.type == 2
    assert h.offset == 17


def test_compressed_ts_header_repr_shows_offset() -> None:
    h = CompressedTimestampHeader(1, 5)
    r = repr(h)
    assert "CompressedTimestampHeader" in r
    assert "+5" in r


# ---------------------------------------------------------------------------
# CompressedTimestampHeader: read
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "msg_type, time_offset",
    [
        (0, 0),
        (1, 5),
        (2, 15),
        (3, 31),
    ],
)
def test_compressed_ts_header_read(msg_type: int, time_offset: int) -> None:
    # bit 7 must be 1; bits 6-5 = msg_type; bits 4-0 = time_offset
    byte = (1 << 7) | (msg_type << 5) | time_offset
    h = CompressedTimestampHeader.read(byte)
    assert h.type == msg_type
    assert h.offset == time_offset


# ---------------------------------------------------------------------------
# CompressedTimestampHeader: write
# ---------------------------------------------------------------------------


def test_compressed_ts_header_write_sets_high_bit() -> None:
    h = CompressedTimestampHeader(0, 0)
    byte_val = h.write()[0]
    assert (byte_val >> 7) & 1 == 1


@pytest.mark.parametrize(
    "msg_type, time_offset",
    [
        (0, 0),
        (1, 5),
        (2, 15),
        (3, 31),
    ],
)
def test_compressed_ts_header_write_read_roundtrip(
    msg_type: int, time_offset: int
) -> None:
    written = CompressedTimestampHeader(msg_type, time_offset).write()
    # Route through RecordHeader.read so the high-bit dispatch is exercised
    restored = RecordHeader.read(written[0])
    assert isinstance(restored, CompressedTimestampHeader)
    assert restored.type == msg_type
    assert restored.offset == time_offset


# ---------------------------------------------------------------------------
# CompressedTimestampHeader: process_message
# ---------------------------------------------------------------------------


def test_compressed_ts_header_process_message_returns_message() -> None:
    """process_message should read data from the buffer and return a Message."""
    # Set up a minimal definition for FileCreator (msg_type=49)
    defn_header = DefinitionHeader(0)
    definition = Definition(defn_header)
    definition.number = 49  # FileCreator
    definition.byte_order = Definition.LITTLE
    definition.fields = Fields([UInt16(0)])  # software_version

    definitions = {0: definition}
    buf = BytesIO(struct.pack("<H", 42))

    h = CompressedTimestampHeader(0, 5)
    msg = h.process_message(definitions, buf)

    assert isinstance(msg, FileCreator)
    assert msg.software_version == 42
