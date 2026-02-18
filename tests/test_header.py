"""Tests for fit.structure.header."""

from __future__ import annotations

import struct

import pytest

from fit.exceptions import BodyFormatError
from fit.structure.crc import compute_crc
from fit.structure.header import Header


def _make_12_byte(data_size: int = 0, protocol: int = 16, profile: int = 1005) -> bytes:
    return struct.pack("<BBHL4s", 12, protocol, profile, data_size, b".FIT")


def _make_14_byte(data_size: int = 0) -> bytes:
    body = struct.pack("<BBHL4s", 14, 16, 1005, data_size, b".FIT")
    return body + struct.pack("<H", compute_crc(body))


# ---------------------------------------------------------------------------
# Initial state
# ---------------------------------------------------------------------------


def test_header_initial_bool_is_false() -> None:
    assert not Header()


def test_header_initial_data_type_is_fit() -> None:
    assert Header().data_type == b".FIT"


def test_header_initial_is_valid() -> None:
    assert Header().valid


# ---------------------------------------------------------------------------
# Read
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "make_fn, expected_size, expected_data_size",
    [
        (_make_12_byte, 12, 0),
        (_make_14_byte, 14, 0),
    ],
)
def test_header_read_size(
    make_fn: object, expected_size: int, expected_data_size: int
) -> None:
    h = Header()
    h.read(make_fn())  # type: ignore[operator]
    assert h.size == expected_size
    assert h.data_size == expected_data_size
    assert h.valid
    assert bool(h)


def test_header_read_14_byte_data_size() -> None:
    h = Header()
    h.read(_make_14_byte(data_size=256))
    assert h.data_size == 256


def test_header_read_14_byte_invalid_crc_raises() -> None:
    body = struct.pack("<BBHL4s", 14, 16, 1005, 0, b".FIT")
    bad_crc = struct.pack("<H", compute_crc(body) ^ 0x0001)
    with pytest.raises(BodyFormatError):
        Header().read(body + bad_crc)


def test_header_read_14_byte_zero_crc_skips_check() -> None:
    body = struct.pack("<BBHL4s", 14, 16, 1005, 0, b".FIT")
    Header().read(body + struct.pack("<H", 0))  # must not raise


# ---------------------------------------------------------------------------
# Write
# ---------------------------------------------------------------------------


def test_header_write_length_is_14() -> None:
    h = Header()
    h.data_size = 0
    assert len(h.write()) == 14


def test_header_write_updates_size_to_14() -> None:
    h = Header()
    h.data_size = 0
    h.write()
    assert h.size == 14


def test_header_write_crc_is_correct() -> None:
    h = Header()
    h.data_size = 42
    result = h.write()
    assert struct.unpack("<H", result[12:])[0] == compute_crc(result[:12])


# ---------------------------------------------------------------------------
# total_size
# ---------------------------------------------------------------------------


def test_header_total_size() -> None:
    h = Header()
    h.read(_make_14_byte(data_size=100))
    # 14 (header) + 100 (data) + 2 (trailing CRC)
    assert h.total_size == 116
