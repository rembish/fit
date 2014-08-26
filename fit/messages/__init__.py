from re import match

from fit.record.fields import Fields
from fit.types import Type
from fit.types.dynamic import DynamicField
from fit.utils import get_known


class Meta(dict):
    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value


class FieldProxy(object):
    def __init__(self, number, key):
        self.number = number
        self.key = key

    def __get__(self, instance, owner):
        main_key = instance._get_name(self.number)

        value = instance._data.get(main_key, None)
        if value is None:
            return None

        field = instance._get_type(self.number)

        if self.key != main_key:  # Subfield
            dynamic_field = instance._meta.model[self.number]
            referred_key = dynamic_field.referred
            referred_value = instance[referred_key]
            subfield = dynamic_field.get_subfield(referred_value)

            if not subfield or self.key != subfield.name:
                return None

            return instance._meta.subfields[self.key]._load(value)
        return field._load(value)

    def __set__(self, instance, value):
        if value is None:
            return self.__delete__(instance)

        field = instance._get_type(self.number)
        main_key = instance._get_name(self.number)

        if self.key != main_key:  # Subfield
            dynamic_field = instance._meta.model[self.number]
            referred_key = dynamic_field.referred
            referred_value = instance[referred_key]
            subfield = dynamic_field.get_subfield(referred_value)

            if self.key != subfield.name:
                raise AttributeError("Irrelevant subfield '%s'" % self.key)

            data = instance._meta.subfields[self.key]._save(value)
        else:
            data = field._save(value)

        instance._data[main_key] = data

    def __delete__(self, instance):
        instance._data[self.key] = None


class MessageMeta(type):
    def __new__(mcs, name, bases, attrs):
        meta = Meta(attrs.pop("_meta", {}))
        meta.model = meta.get("model", {})
        meta.names = meta.get("names", {})
        meta.subfields = meta.get("subfields", {})

        inherit = True
        if "_meta" in attrs:
            inherit = meta.get("inherit", True)

        for base in bases:
            if hasattr(base, "_meta") and inherit:
                meta.model.update(base._meta.get("model", {}))
                meta.names.update(base._meta.get("names", {}))
                meta.subfields.update(base._meta.get("subfields", {}))

        for key, value in attrs.items():
            if isinstance(value, DynamicField):
                for subfield in value.variants.values():
                    subfield.type = subfield.type or value.base.__class__
                    meta.subfields[subfield.name] = subfield.type(
                        value.number, **subfield.kwargs)

            if isinstance(value, Type):
                meta.model[value.number] = value
                meta.names[value.number] = key

        for key in meta.names.values():
            attrs.pop(key, None)

        attrs['_meta'] = meta
        instance = super(MessageMeta, mcs).__new__(mcs, name, bases, attrs)

        for number, key in meta.names.items():
            setattr(instance, key, FieldProxy(number, key))
        for name, subfield in meta.subfields.items():
            setattr(instance, name, FieldProxy(subfield.number, name))

        return instance


class Message(object):
    __metaclass__ = MessageMeta
    _meta = Meta()

    msg_type = None

    def __init__(self, definition=None, **data):
        if not definition:
            from fit.record.definition import Definition
            from fit.record.header import DefinitionHeader

            definition = Definition(DefinitionHeader(self.msg_type))
            definition.fields = Fields(self._meta.model.values())
            definition.number = self.msg_type

        self._data = {}
        self._definition = definition

        self._unknowns = {}

        for key, value in data.items():
            self[key] = value

    def __repr__(self):
        data = {}
        for field in self.definition.fields:
            name = self._get_name(field.number)
            field = self._get_type(field.number)
            field_name = name
            if name.startswith("unknown_"):
                field_name = "%s[%d]" % (
                    field.__class__.__name__,
                    field.number
                )

            data[field_name] = "%s%s" % (
                getattr(self, name),
                getattr(field, "units", None) or ""
            )

        normal_part = (' %s' % ' '.join(
            "%s=%s" % (key, value)
            for key, value in data.items()
        )).rstrip()

        dynamic_part = (' %s' % ' '.join(
            "%s=%s" % (key, self[key])
            for key in self._meta.subfields.keys()
            if self[key] is not None
        )).rstrip()

        return '<%s.%s[%d]%s%s>' % (
            self.__module__.split(".")[-1],
            self.__class__.__name__,
            self.msg_type,
            normal_part, dynamic_part
        )

    def __setitem__(self, key, value):
        self._get_number(key)
        setattr(self, key, value)

    def __getitem__(self, key):
        self._get_number(key)
        return getattr(self, key)

    def __delitem__(self, key):
        self._get_number(key)
        delattr(self, key)

    def _get_name(self, number):
        if number not in self._meta.names:
            return "unknown_%d" % number
        return self._meta.names[number]

    def _get_type(self, number):
        if number not in self._meta.model:
            return self._unknowns[number]
        return self._meta.model[number]

    def _get_number(self, name):
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
    def definition(self):
        fields = Fields(
            field for number, field in self._meta.model.items()
            if getattr(self, self._get_name(number)) is not None
        )
        for number, field in self._unknowns.items():
            if getattr(self, self._get_name(number)) is not None:
                fields.append(field)

        self._definition.fields = fields
        return self._definition

    def read(self, read_buffer, model):
        for field in model:
            unknown = None
            if field.number not in self._meta.names:
                self._unknowns[field.number] = field
                unknown = self._get_name(field.number)

            resolved = self._get_type(field.number)
            resolved.size = field.size
            self._data[self._get_name(field.number)] = field.read(
                read_buffer, architecture=self._definition.architecture)

            if unknown:
                setattr(self, unknown, self._data[unknown])

    def write(self, index, model=None):
        from fit.record.header import DataHeader

        model = model or self.definition.fields
        write_buffer = DataHeader(index).write()
        for field in model:
            value = self[self._get_name(field.number)]
            data = field._save(value)
            write_buffer += field.write(data)
        return write_buffer


KNOWN = get_known(__name__, Message, key="msg_type")


def register(message_cls):
    global KNOWN

    if not issubclass(message_cls, Message):
        raise ValueError(
            "%s should be subclass of Message" % message_cls.__name__)
    if not isinstance(message_cls.msg_type, int):
        raise ValueError(
            "%s should have defined message type" % message_cls.__name__)
    if not message_cls._meta.model:
        raise ValueError(
            "%s should have not empty model" % message_cls.__name__)

    KNOWN[message_cls.msg_type] = message_cls
