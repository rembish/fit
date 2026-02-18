"""Tests for fit.messages — metaclass, FieldProxy, and the message registry."""

from __future__ import annotations

from datetime import datetime

import pytest

from fit.messages import KNOWN, Message, register
from fit.messages.common import FileCreator, FileId
from fit.messages.generic import GenericMessage
from fit.record.definition import Definition
from fit.record.header import DefinitionHeader
from fit.types.general import UInt8, UInt16, UInt32

# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------


def test_known_registry_is_populated() -> None:
    assert len(KNOWN) > 0


@pytest.mark.parametrize(
    "msg_type, expected_cls",
    [(0, FileId), (49, FileCreator)],
)
def test_known_registry_contains(msg_type: int, expected_cls: type) -> None:
    assert msg_type in KNOWN
    assert KNOWN[msg_type] is expected_cls


# ---------------------------------------------------------------------------
# MessageMeta / FieldProxy
# ---------------------------------------------------------------------------


def test_field_becomes_proxy_descriptor() -> None:
    class MyMsg(Message):
        msg_type = 9999
        speed = UInt16(0)

    msg = MyMsg()
    assert msg.speed is None
    msg.speed = 1234
    assert msg.speed == 1234


def test_subclass_inherits_parent_fields() -> None:
    class Base(Message):
        msg_type = 9998
        field_a = UInt8(0)

    class Child(Base):
        msg_type = 9997
        field_b = UInt8(1)

    child = Child()
    child.field_a = 10
    child.field_b = 20
    assert child.field_a == 10
    assert child.field_b == 20


# ---------------------------------------------------------------------------
# Message basics
# ---------------------------------------------------------------------------


def test_message_set_and_get_field() -> None:
    msg = FileCreator()
    msg.software_version = 100
    assert msg.software_version == 100


def test_message_set_none_clears_field() -> None:
    msg = FileCreator()
    msg.software_version = 100
    msg.software_version = None
    assert msg.software_version is None


def test_message_setitem_getitem() -> None:
    msg = FileCreator()
    msg["software_version"] = 200
    assert msg["software_version"] == 200


def test_message_contains_int_key() -> None:
    assert 0 in FileCreator()  # software_version field number


def test_message_unknown_key_raises() -> None:
    with pytest.raises(KeyError):
        _ = FileCreator()["nonexistent_field"]


def test_message_repr_contains_class_name() -> None:
    assert "FileCreator" in repr(FileCreator())


# ---------------------------------------------------------------------------
# register()
# ---------------------------------------------------------------------------


def test_register_custom_message() -> None:
    class CustomMsg(Message):
        msg_type = 8888
        value = UInt32(0)

    register(CustomMsg)
    assert KNOWN[8888] is CustomMsg
    del KNOWN[8888]  # cleanup


def test_register_non_message_subclass_raises() -> None:
    with pytest.raises(ValueError, match="subclass of Message"):
        register(object)  # type: ignore[arg-type]


def test_register_no_msg_type_raises() -> None:
    class BadMsg(Message):
        pass

    with pytest.raises(ValueError):
        register(BadMsg)


def test_register_no_fields_raises() -> None:
    class BadMsg(Message):
        msg_type = 7777

    with pytest.raises(ValueError):
        register(BadMsg)


# ---------------------------------------------------------------------------
# FileId.create
# ---------------------------------------------------------------------------


def test_file_id_create_sets_filetype() -> None:
    assert FileId.create(4).filetype == 4


def test_file_id_create_sets_time_created() -> None:
    assert isinstance(FileId.create(4).time_created, datetime)


# ---------------------------------------------------------------------------
# GenericMessage
# ---------------------------------------------------------------------------


def test_generic_message_msg_type_starts_none() -> None:
    defn = Definition(DefinitionHeader(0))
    defn.number = 0
    assert GenericMessage(defn).msg_type is None
