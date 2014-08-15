from copy import copy
from importlib import import_module
from inspect import getmembers, isclass
from pkgutil import iter_modules

from fit.type import Type


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
        self.definition = definition

    def __repr__(self):
        return '<%s[%d] %s>' % (
            self.__class__.__name__, self.msg_type,
            ' '.join("%s=%s" % (
                self._meta.names[field.number],
                self._meta.model[field.number].readable(getattr(
                    self, self._meta.names[field.number]))
            ) for field in self.definition.fields
                if getattr(self, self._meta.names[field.number]) is not None)
        )

    @property
    def compressed_definition(self):
        from fit.record.definition import Fields

        new = copy(self.definition)
        new.fields = Fields()
        for field in self.definition.fields:
            value = getattr(self, self._meta.names[field.number])
            if value is not None:
                new.fields.append(field)

        return new

    def read(self, buffer):
        unknown = 0
        for field in self.definition.fields:
            if field.number not in self._meta.names:
                self._meta.names[field.number] = "unknown_%d" % unknown
                self._meta.model[field.number] = field
                unknown += 1

            setattr(
                self, self._meta.names[field.number],
                field.read(
                    buffer, architecture=self.definition.architecture))

    def write(self, index):
        from fit.record.header import DataHeader

        buffer = DataHeader(index).write()
        for field in self.definition.fields:
            value = getattr(self, self._meta.names[field.number])
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
