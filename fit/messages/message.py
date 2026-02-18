"""FIT message base class, metaclass machinery, and message registry."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from dataclasses import field as dc_field
from re import match
from typing import Any

from fit.record import TIMESTAMP_FIELD_NAME, TIMESTAMP_FIELD_NUM, TIMESTAMP_MASK
from fit.record.fields import Fields
from fit.types import Type as FitType
from fit.types.array import Array
from fit.types.dynamic import Dynamic
from fit.types.extended import LocalDateTime
from fit.utils import get_known

__all__ = ["KNOWN", "Message", "register"]


@dataclass
class Meta:
    """Field registry for a :class:`Message` subclass.

    Attributes:
        model: Maps field number → :class:`~fit.types.Type` instance.
        names: Maps field number → attribute name.
        subfields: Maps subfield name → resolved :class:`~fit.types.Type` instance.
        inherit: Whether to copy parent-class fields into this class (default ``True``).
    """

    model: dict[int, FitType] = dc_field(default_factory=dict)
    names: dict[int, str] = dc_field(default_factory=dict)
    subfields: dict[str, Any] = dc_field(default_factory=dict)
    inherit: bool = True


class FieldProxy:
    """Descriptor that routes attribute access to a message's ``_data`` store.

    Handles both regular fields and sub-fields of :class:`~fit.types.dynamic.Dynamic`
    types.

    Args:
        number: FIT field number.
        key: Attribute name on the message class.
    """

    def __init__(self, number: int, key: str) -> None:
        self.number: int = number
        self.key: str = key

    def __get__(self, instance: Any, owner: type) -> Any:
        if instance is None:
            return self
        main_key = instance._get_name(self.number)

        value = instance._data.get(main_key, None)
        if value is None:
            return None

        field = instance._get_type(self.number)

        if self.key != main_key:  # Sub-field
            dynamic_field = instance._meta.model[self.number]
            referred_key = dynamic_field.referred
            referred_value = instance[referred_key]
            subfield = dynamic_field.get_subfield(referred_value)

            if not subfield or self.key != subfield.name:
                return None

            return instance._meta.subfields[self.key]._load(value)
        return field._load(value)

    def __set__(self, instance: Any, value: Any) -> None:
        if value is None:
            return self.__delete__(instance)

        field = instance._get_type(self.number)
        main_key = instance._get_name(self.number)

        if self.key != main_key:  # Sub-field
            dynamic_field = instance._meta.model[self.number]
            referred_key = dynamic_field.referred
            referred_value = instance[referred_key]
            subfield = dynamic_field.get_subfield(referred_value)

            if self.key != subfield.name:
                raise AttributeError(f"Irrelevant subfield '{self.key}'")

            data = instance._meta.subfields[self.key]._save(value)
        else:
            data = field._save(value)

        instance._data[main_key] = data

    def __delete__(self, instance: Any) -> None:
        instance._data[self.key] = None


class MessageMeta(type):
    """Metaclass for :class:`Message` that registers field descriptors at class creation."""

    def __new__(
        cls,
        name: str,
        bases: tuple[type, ...],
        attrs: dict[str, Any],
    ) -> MessageMeta:
        raw = attrs.pop("_meta", None)
        meta = raw if isinstance(raw, Meta) else Meta()

        for base in bases:
            if hasattr(base, "_meta") and meta.inherit:
                meta.model.update(base._meta.model)
                meta.names.update(base._meta.names)
                meta.subfields.update(base._meta.subfields)

        for key, value in attrs.items():
            if isinstance(value, Dynamic):
                for subfield in value.variants.values():
                    subfield.type = subfield.type or value.base.__class__
                    meta.subfields[subfield.name] = subfield.type(
                        value.number, **subfield.kwargs
                    )

            if isinstance(value, FitType):
                meta.model[value.number] = value
                meta.names[value.number] = key

        for key in meta.names.values():
            attrs.pop(key, None)

        attrs["_meta"] = meta
        instance = super().__new__(cls, name, bases, attrs)

        for number, key in meta.names.items():
            setattr(instance, key, FieldProxy(number, key))
        for sf_name, sf_type in meta.subfields.items():
            setattr(instance, sf_name, FieldProxy(sf_type.number, sf_name))

        return instance


class Message(metaclass=MessageMeta):
    """Base class for all FIT protocol messages.

    Each concrete subclass declares its fields as class-level
    :class:`~fit.types.Type` instances. :class:`MessageMeta` replaces them
    with :class:`FieldProxy` descriptors so that reading/writing goes through
    the type's ``_load`` / ``_save`` converters.

    Args:
        definition: The :class:`~fit.record.definition.Definition` that
            describes this message's field layout.  If omitted, one is built
            from :attr:`_meta`.
        **data: Initial field values (keyword arguments).
    """

    _meta: Meta
    msg_type: int | None = None

    def __init__(
        self,
        definition: object | None = None,
        **data: Any,
    ) -> None:
        if not definition:
            from fit.record.definition import Definition
            from fit.record.header import DefinitionHeader

            definition = Definition(DefinitionHeader(self.msg_type or 0))
            definition.fields = Fields(self._meta.model.values())  # type: ignore[attr-defined]
            definition.number = self.msg_type  # type: ignore[attr-defined]

        self._data: dict[str, Any] = {}
        self._definition = definition
        self._unknowns: dict[int, Any] = {}

        for key, value in data.items():
            self[key] = value

    def __repr__(self) -> str:
        data: dict[str, str] = {}
        for field in self.definition.fields:  # type: ignore[union-attr]
            field_name_raw = self._get_name(field.number)
            field_obj = self._get_type(field.number)
            display_name = field_name_raw
            if field_name_raw.startswith("unknown_"):
                display_name = f"{field_obj.__class__.__name__}[{field_obj.number}]"

            data[display_name] = "{}{}".format(
                getattr(self, field_name_raw),
                getattr(field_obj, "units", None) or "",
            )

        normal_part = (" " + " ".join(f"{k}={v}" for k, v in data.items())).rstrip()

        dynamic_part = (
            " "
            + " ".join(
                f"{key}={self[key]}"
                for key in self._meta.subfields
                if self[key] is not None
            )
        ).rstrip()

        return (
            f"<{self.__module__.split('.')[-1]}."
            f"{self.__class__.__name__}[{self.msg_type}]"
            f"{normal_part}{dynamic_part}>"
        )

    def __setitem__(self, key: str | int, value: Any) -> None:
        if isinstance(key, int):
            key = self._get_name(key)
        self._get_number(key)
        setattr(self, key, value)

    def __getitem__(self, key: str | int) -> Any:
        if isinstance(key, int):
            key = self._get_name(key)
        self._get_number(key)
        return getattr(self, key)

    def __delitem__(self, key: str | int) -> None:
        if isinstance(key, int):
            key = self._get_name(key)
        self._get_number(key)
        delattr(self, key)

    def __contains__(self, key: str | int) -> bool:
        if isinstance(key, int):
            key = self._get_name(key)
        return hasattr(self, key)

    def __iter__(self) -> Iterator[Any]:
        for field in self.definition.fields:  # type: ignore[union-attr]
            yield self[field.number]

    def __len__(self) -> int:
        return len(self.definition.fields)  # type: ignore[arg-type]

    def _get_name(self, number: int) -> str:
        if number not in self._meta.names:
            return f"unknown_{number}"
        return self._meta.names[number]

    def _get_type(self, number: int) -> Any:
        if number not in self._meta.model:
            return self._unknowns[number]
        return self._meta.model[number]

    def _get_number(self, name: str) -> int | None:
        if name in self._meta.subfields:
            return None

        for number, other in self._meta.names.items():
            if name == other:
                return number

        if match(r"unknown_\d+", name):
            number = int(name.split("_")[-1])
            if number in self._unknowns:
                return number

        raise KeyError(name)

    @property
    def definition(self) -> Any:
        """Return the effective definition with only non-None fields."""
        fields = Fields(
            field
            for number, field in self._meta.model.items()
            if getattr(self, self._get_name(number)) is not None
        )
        for number, field in self._unknowns.items():
            if getattr(self, self._get_name(number)) is not None:
                fields.append(field)

        for field in fields:
            if isinstance(field, Array):
                field.size = field.value_type.size * len(
                    getattr(self, self._get_name(field.number))
                )

        self._definition.fields = fields  # type: ignore[attr-defined]
        return self._definition

    def read(self, read_buffer: Any, model: Any) -> None:
        """Populate this message by reading field values from *read_buffer*.

        Args:
            read_buffer: Readable binary stream.
            model: Iterable of field descriptors (e.g. a :class:`~fit.record.fields.Fields`).
        """
        for field in model:
            unknown = None
            if field.number not in self._meta.names:
                self._unknowns[field.number] = field
                unknown = self._get_name(field.number)

            resolved = self._get_type(field.number)
            resolved.size = field.size
            self._data[self._get_name(field.number)] = field.read(
                read_buffer, architecture=self._definition.architecture  # type: ignore[union-attr, attr-defined]
            )

            if unknown:
                setattr(self, unknown, self._data[unknown])

    def write(self, index: int, model: Any = None) -> bytes:
        """Serialise this message to bytes.

        Args:
            index: Local message type index used when writing the data header.
            model: Optional field list override; defaults to :attr:`definition` fields.

        Returns:
            Packed bytes: data header + all field values.
        """
        from fit.record.header import DataHeader

        model = model or self.definition.fields
        write_buffer = DataHeader(index).write()
        for field in model:
            value = self[self._get_name(field.number)]
            data = field._save(value)
            write_buffer += field.write(data)
        return write_buffer

    def process_timestamp(
        self,
        timestamp: int,
        offset: int,
    ) -> tuple[int, int]:
        """Update the running timestamp from this message's content.

        Handles both regular timestamp fields and compressed-timestamp headers.

        Args:
            timestamp: Current running timestamp value.
            offset: Current 5-bit offset within the timestamp.

        Returns:
            Updated ``(timestamp, offset)`` pair.
        """
        if TIMESTAMP_FIELD_NUM in self:
            timestamp = self._data.get(self._get_name(TIMESTAMP_FIELD_NUM), timestamp)
            offset = timestamp & TIMESTAMP_MASK

        if not hasattr(self._definition, "offset"):
            return timestamp, offset

        # Compressed timestamp: roll the offset forward
        timestamp += (self._definition.offset - offset) & TIMESTAMP_MASK  # type: ignore[union-attr]
        offset = self._definition.offset  # type: ignore[union-attr]
        self._meta.names[TIMESTAMP_FIELD_NUM] = TIMESTAMP_FIELD_NAME
        ts_field = self._meta.model[TIMESTAMP_FIELD_NUM] = LocalDateTime(
            TIMESTAMP_FIELD_NUM
        )
        setattr(self, TIMESTAMP_FIELD_NAME, ts_field._load(timestamp))

        return timestamp, offset


KNOWN: dict[Any, type[Message]] = get_known("fit.messages", Message, key="msg_type")


def register(message_cls: type[Message]) -> None:
    """Register a custom :class:`Message` subclass in the global message table.

    Args:
        message_cls: The message class to register. Must be a :class:`Message`
            subclass with an integer :attr:`msg_type` and a non-empty model.

    Raises:
        ValueError: If any of the preconditions are not met.
    """
    if not issubclass(message_cls, Message):
        raise ValueError(f"{message_cls.__name__} should be subclass of Message")
    if not isinstance(message_cls.msg_type, int):
        raise ValueError(f"{message_cls.__name__} should have defined message type")
    if not message_cls._meta.model:
        raise ValueError(f"{message_cls.__name__} should have non-empty model")

    KNOWN[message_cls.msg_type] = message_cls
