"""Tests for fit.structure.crc."""

from __future__ import annotations

import struct

import pytest

from fit.structure.crc import Crc, compute_crc

# ---------------------------------------------------------------------------
# compute_crc
# ---------------------------------------------------------------------------


def test_compute_crc_empty_bytes_is_zero() -> None:
    assert compute_crc(b"") == 0


def test_compute_crc_returns_uint16() -> None:
    result = compute_crc(b"\x00")
    assert isinstance(result, int)
    assert 0 <= result <= 0xFFFF


def test_compute_crc_deterministic() -> None:
    data = b"hello fit"
    assert compute_crc(data) == compute_crc(data)


def test_compute_crc_different_inputs_differ() -> None:
    assert compute_crc(b"abc") != compute_crc(b"xyz")


def test_compute_crc_fit_magic_nonzero() -> None:
    assert compute_crc(b".FIT") != 0


@pytest.mark.parametrize(
    "data", [b"\x01", b"\xff", b"\x0e\x10\xed\x03\x00\x00\x00\x00.FIT"]
)
def test_compute_crc_idempotent(data: bytes) -> None:
    assert compute_crc(data) == compute_crc(data)


# ---------------------------------------------------------------------------
# Crc
# ---------------------------------------------------------------------------


def test_crc_initial_value_is_none() -> None:
    assert Crc().value is None


def test_crc_initial_size_is_2() -> None:
    assert Crc().size == 2


def test_crc_bool_false_when_unset() -> None:
    assert not Crc()


def test_crc_bool_true_when_set() -> None:
    crc = Crc()
    crc.value = 0x1234
    assert crc


def test_crc_read() -> None:
    crc = Crc()
    crc.read(struct.pack("<H", 0xABCD))
    assert crc.value == 0xABCD


def test_crc_write_unset_gives_zero() -> None:
    assert Crc().write() == struct.pack("<H", 0)


def test_crc_write_set_value() -> None:
    crc = Crc()
    crc.value = 0x1234
    assert crc.write() == struct.pack("<H", 0x1234)


def test_crc_check_correct() -> None:
    data = b"test data for crc"
    crc = Crc()
    crc.value = compute_crc(data)
    assert crc.check(data)


def test_crc_check_wrong_value() -> None:
    data = b"test data"
    crc = Crc()
    crc.value = compute_crc(data) ^ 0x0001
    assert not crc.check(data)


def test_crc_repr_contains_class_name() -> None:
    assert "Crc" in repr(Crc())


def test_crc_repr_contains_value_when_set() -> None:
    crc = Crc()
    crc.value = 42
    assert "42" in repr(crc)
