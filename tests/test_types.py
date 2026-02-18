"""Tests for fit.types: base types, numeric types, array, dynamic, and helpers."""

from __future__ import annotations

import struct
from io import BytesIO

import pytest

from fit.types.array import Array
from fit.types.composite import ComponentField, Composite
from fit.types.dynamic import Dynamic, SubField
from fit.types.general import (
    Enum,
    SInt8,
    SInt32,
    String,
    UInt8,
    UInt16,
    UInt32,
    UInt32Z,
)
from fit.types.helpers import KnownMixin, degrees

# ---------------------------------------------------------------------------
# Type base
# ---------------------------------------------------------------------------


def test_type_repr() -> None:
    assert "UInt8" in repr(UInt8(5))
    assert "5" in repr(UInt8(5))


@pytest.mark.parametrize("num,equal", [(3, True), (4, False)])
def test_type_eq_by_number(num: int, equal: bool) -> None:
    assert (UInt8(3) == UInt8(num)) == equal


def test_type_hashable_in_set() -> None:
    # Type.__hash__ must exist so instances can be put in sets
    s = {UInt8(0), UInt16(1), UInt32(2)}
    assert len(s) == 3


def test_type_read_invalid_sentinel_returns_none() -> None:
    assert UInt8(0).read(BytesIO(bytes([0xFF]))) is None


def test_type_write_none_uses_invalid() -> None:
    assert UInt8(0).write(None) == bytes([0xFF])


def test_type_read_write_round_trip() -> None:
    t = UInt16(1)
    packed = t.write(0x1234)
    assert t.read(BytesIO(packed)) == 0x1234


# ---------------------------------------------------------------------------
# BinaryType (scale / offset)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "value,scale,offset,expected",
    [
        (5000, 1000, None, 5.0),
        (2500, 5, 500, 0.0),  # altitude: raw/5 - 500
    ],
)
def test_binary_type_load(
    value: int, scale: float, offset: float | None, expected: float
) -> None:
    t = UInt32(0) * scale
    if offset is not None:
        t = t + offset
    assert t._load(value) == pytest.approx(expected)


@pytest.mark.parametrize(
    "value,scale,expected_raw",
    [
        (5.0, 1000, 5000),
        (0.0, 5, 0),
    ],
)
def test_binary_type_save(value: float, scale: float, expected_raw: int) -> None:
    t = UInt32(0) * scale
    assert t._save(value) == expected_raw


def test_binary_type_mul_sets_scale() -> None:
    assert (UInt32(0) * 1000).scale == 1000.0


def test_binary_type_mul_sets_units() -> None:
    assert (UInt16(0) * "m/s").units == "m/s"


def test_binary_type_add_sets_offset() -> None:
    assert (UInt16(0) + 500).offset == 500.0


def test_binary_type_sub_sets_negative_offset() -> None:
    assert (UInt16(0) - 100).offset == -100.0


def test_binary_type_no_scale_passthrough() -> None:
    t = UInt8(0)
    assert t._load(42) == 42
    assert t._save(42) == 42


# ---------------------------------------------------------------------------
# Enum
# ---------------------------------------------------------------------------


def test_enum_load_known_value() -> None:
    e = Enum(0)
    e.__class__.variants = {1: "running"}
    assert e._load(1) == "running"


def test_enum_load_unknown_passthrough() -> None:
    e = Enum(0)
    e.__class__.variants = {}
    assert e._load(99) == 99


# ---------------------------------------------------------------------------
# SInt8
# ---------------------------------------------------------------------------


def test_sint8_read_negative() -> None:
    assert SInt8(0).read(BytesIO(struct.pack("<b", -10))) == -10


def test_sint8_invalid_sentinel_is_none() -> None:
    assert SInt8(0).read(BytesIO(bytes([0x7F]))) is None


# ---------------------------------------------------------------------------
# UInt32Z
# ---------------------------------------------------------------------------


def test_uint32z_zero_is_none() -> None:
    assert UInt32Z(0).read(BytesIO(struct.pack("<I", 0))) is None


def test_uint32z_nonzero_reads_value() -> None:
    assert UInt32Z(0).read(BytesIO(struct.pack("<I", 0xDEADBEEF))) == 0xDEADBEEF


# ---------------------------------------------------------------------------
# String
# ---------------------------------------------------------------------------


def test_string_format_property() -> None:
    assert String(0, size=10).format == "10s"


def test_string_default_size_is_1() -> None:
    assert String(0).size == 1


# ---------------------------------------------------------------------------
# Array
# ---------------------------------------------------------------------------


def test_array_count() -> None:
    assert Array(UInt16(0), size=8).count == 4


def test_array_read_multiple_values() -> None:
    arr = Array(UInt16(0), size=4)
    assert arr.read(BytesIO(struct.pack("<HH", 10, 20))) == [10, 20]


def test_array_write_multiple_values() -> None:
    arr = Array(UInt16(0), size=4)
    assert arr.write([10, 20]) == struct.pack("<HH", 10, 20)


def test_array_write_returns_bytes() -> None:
    assert isinstance(Array(UInt8(0), size=3).write([1, 2, 3]), bytes)


# ---------------------------------------------------------------------------
# Dynamic / SubField
# ---------------------------------------------------------------------------


def test_dynamic_repr() -> None:
    base = UInt32(3) * 2
    d = Dynamic(base, referred_to="activity_type", walking=SubField("steps"))
    assert "Dynamic" in repr(d)


def test_dynamic_type_delegates_to_base() -> None:
    base = UInt32(3)
    d = Dynamic(base, referred_to="activity_type", walking=SubField("steps"))
    assert d.type == base.type


def test_dynamic_read_delegates_to_base() -> None:
    base = UInt32(3)
    d = Dynamic(base, referred_to="activity_type", walking=SubField("steps"))
    buf = BytesIO(struct.pack("<I", 42))
    assert d.read(buf) == 42


def test_dynamic_write_delegates_to_base() -> None:
    base = UInt32(3)
    d = Dynamic(base, referred_to="activity_type", walking=SubField("steps"))
    assert d.write(42) == struct.pack("<I", 42)


def test_dynamic_get_subfield_match() -> None:
    d = Dynamic(UInt32(3), referred_to="x", walking=SubField("steps"))
    sf = d.get_subfield("walking")
    assert sf is not None
    assert sf.name == "steps"


def test_dynamic_get_subfield_no_match_returns_none() -> None:
    d = Dynamic(UInt32(3), referred_to="x", walking=SubField("steps"))
    assert d.get_subfield("unknown") is None


# ---------------------------------------------------------------------------
# KnownMixin
# ---------------------------------------------------------------------------


class _KnownType(KnownMixin, UInt8):
    known = {1: "foo", 2: "bar"}


@pytest.mark.parametrize("raw,expected", [(1, "foo"), (2, "bar"), (99, 99)])
def test_known_mixin_load(raw: int, expected: object) -> None:
    assert _KnownType(0)._load(raw) == expected


@pytest.mark.parametrize("name,expected", [("foo", 1), ("bar", 2), (42, 42)])
def test_known_mixin_save(name: object, expected: int) -> None:
    assert _KnownType(0)._save(name) == expected


# ---------------------------------------------------------------------------
# degrees helper
# ---------------------------------------------------------------------------


def test_degrees_returns_sint32() -> None:
    assert isinstance(degrees(3), SInt32)


def test_degrees_units() -> None:
    assert degrees(3).units == "°"


def test_degrees_scale_is_positive() -> None:
    scale = degrees(3).scale
    assert scale is not None and scale > 0


# ---------------------------------------------------------------------------
# ComponentField
# ---------------------------------------------------------------------------


def test_component_field_extract_from_int() -> None:
    cf = ComponentField(bits=4, offset=0)
    assert cf.extract(0b10110101) == 5  # bits 0-3 = 0101 = 5


def test_component_field_extract_with_offset() -> None:
    cf = ComponentField(bits=4, offset=4)
    assert cf.extract(0b10110101) == 11  # bits 4-7 = 1011 = 11


def test_component_field_extract_with_scale() -> None:
    cf = ComponentField(bits=12, offset=0) * 100
    # raw=500, physical = 500 / 100 = 5.0
    assert cf.extract(500) == pytest.approx(5.0)


def test_component_field_extract_from_list() -> None:
    # [0x34, 0x12] → little-endian int 0x1234 = 4660
    cf = ComponentField(bits=12, offset=0)
    assert cf.extract([0x34, 0x12]) == 0x234  # bits 0-11 = 0x234 = 564


def test_component_field_extract_none_returns_none() -> None:
    cf = ComponentField(bits=8, offset=0)
    assert cf.extract(None) is None


def test_component_field_pack_into_int() -> None:
    cf = ComponentField(bits=4, offset=0)
    result = cf.pack_into(0b11110000, 5)
    assert result & 0b00001111 == 5
    assert result & 0b11110000 == 0b11110000  # upper bits preserved


def test_component_field_pack_into_with_scale() -> None:
    cf = ComponentField(bits=12, offset=0) * 100
    # value=5.0, raw_component = round(5.0 * 100) = 500
    result = cf.pack_into(0, 5.0)
    assert result & 0xFFF == 500


def test_component_field_pack_into_list() -> None:
    cf = ComponentField(bits=8, offset=0)
    result = cf.pack_into([0x00, 0x00], 42)
    assert isinstance(result, list)
    assert result[0] == 42
    assert result[1] == 0


def test_component_field_pack_into_bytes() -> None:
    cf = ComponentField(bits=8, offset=0)
    result = cf.pack_into(bytes([0x00, 0x00]), 42)
    assert isinstance(result, bytes)
    assert result[0] == 42
    assert result[1] == 0


def test_component_field_pack_into_none_raw() -> None:
    cf = ComponentField(bits=8, offset=0)
    result = cf.pack_into(None, 7)
    assert result == 7


def test_component_field_extract_pack_roundtrip() -> None:
    cf = ComponentField(bits=12, offset=0) * 100
    original = 3.75
    packed = cf.pack_into(0, original)
    extracted = cf.extract(packed)
    assert extracted == pytest.approx(original, abs=0.01)


# ---------------------------------------------------------------------------
# Composite
# ---------------------------------------------------------------------------


def test_composite_size_matches_base() -> None:
    from fit.types.array import Array

    base = Array(UInt8(8), size=3)
    c = Composite(base, speed=ComponentField(bits=12) * 100)
    assert c.size == 3


def test_composite_read_delegates_to_base() -> None:
    base = Array(UInt16(0), size=4)
    c = Composite(base, x=ComponentField(bits=16))
    buf = BytesIO(struct.pack("<HH", 10, 20))
    assert c.read(buf) == [10, 20]


def test_composite_write_delegates_to_base() -> None:
    base = Array(UInt16(0), size=4)
    c = Composite(base, x=ComponentField(bits=16))
    assert c.write([10, 20]) == struct.pack("<HH", 10, 20)


def test_composite_decompose() -> None:
    # 24-bit composite: speed in bits 0-11, distance in bits 12-23

    base_val = (40 << 12) | 50  # distance=40, speed=50
    b0 = base_val & 0xFF
    b1 = (base_val >> 8) & 0xFF
    b2 = (base_val >> 16) & 0xFF

    c = Composite(
        Array(UInt8(8), size=3),
        speed=ComponentField(bits=12, offset=0) * 100,
        distance=ComponentField(bits=12, offset=12) * 16,
    )
    result = c.decompose([b0, b1, b2])
    assert result["speed"] == pytest.approx(50 / 100)
    assert result["distance"] == pytest.approx(40 / 16)


# ---------------------------------------------------------------------------
# ComponentProxy via Record.compressed_speed_distance
# ---------------------------------------------------------------------------


def test_component_proxy_on_record() -> None:
    """ComponentProxy fields not conflicting with named fields are accessible."""
    from fit.messages.activity import Record

    # 'compressed_speed_distance' components are 'speed' and 'distance',
    # which conflict with Record.speed (field 6) and Record.distance (field 5).
    # So NO ComponentProxy should be installed for those names — they remain
    # FieldProxy descriptors for fields 6 and 5.
    r = Record()
    # Field proxies for speed/distance should still work normally
    r.speed = 5.0
    assert r.speed == pytest.approx(5.0)


def test_composite_field_size_propagation() -> None:
    """Regression: Composite must inherit base.size (was previously always 0)."""
    from fit.types.general import Byte

    base = Array(Byte(8), size=3)
    c = Composite(base, x=ComponentField(bits=8))
    assert c.size == base.size
