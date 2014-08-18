from copy import copy
from importlib import import_module
from inspect import getmembers, isclass
from pkgutil import iter_modules

from fit.record.fields import Fields
from fit.types import Type


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
        return instance._data.get(self.key, None)

    def __set__(self, instance, value):
        instance._data[self.key] = value

    def __delete__(self, instance):
        instance._data[self.key] = None


class MessageMeta(type):
    def __new__(cls, name, bases, attrs):
        meta = Meta()
        meta.model = {}
        meta.names = {}

        for key, value in attrs.items():
            if isinstance(value, Type):
                meta.model[value.number] = value
                meta.names[value.number] = key

        for key in meta.names.values():
            attrs.pop(key)

        attrs['_meta'] = meta
        instance = super(MessageMeta, cls).__new__(cls, name, bases, attrs)

        for number, key in meta.names.items():
            setattr(instance, key, FieldProxy(number, key))

        return instance


class Message(object):
    __metaclass__ = MessageMeta

    msg_type = -1

    def __init__(self, definition):
        self._data = {}
        self._definition = definition

        self._unknowns = {}

    def __repr__(self):
        return '<%s.%s[%d] %s>' % (
            self.__module__.split(".")[-1],
            self.__class__.__name__,
            self.msg_type,
            ' '.join("%s=%s" % (
                self._get_name(field.number),
                getattr(self, self._get_name(field.number))
            ) for field in self.definition.fields)
        )

    def _get_name(self, number):
        if number not in self._meta.names:
            return "unknown_%d" % number
        return self._meta.names[number]

    def _get_type(self, number):
        if number not in self._meta.model:
            return self._unknowns[number]
        return self._meta.model[number]

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

    def read(self, buffer, model):
        for field in model:
            if field.number not in self._meta.names:
                self._unknowns[field.number] = field

            setattr(
                self, self._get_name(field.number),
                self._get_type(field.number).read(
                    buffer, architecture=self._definition.architecture))

    def write(self, index, model=None):
        from fit.record.header import DataHeader

        model = model or self.definition
        buffer = DataHeader(index).write()
        for field in model:
            value = getattr(self, self._get_name(field.number))
            buffer += field.write(value)
        return buffer


class GenericMessage(Message):
    def __init__(self, definition):
        super(GenericMessage, self).__init__(definition)
        self.msg_type = None


def get_known():
    main = import_module(__name__)
    known = {}

    for _, module_name, _ in iter_modules(main.__path__, "%s." % __name__):
        module = import_module(module_name)
        for _, obj in getmembers(module, isclass):
            if issubclass(obj, Message):
                known[obj.msg_type] = obj

    return known


KNOWN = get_known()
del get_known
