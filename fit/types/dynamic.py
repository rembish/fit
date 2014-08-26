from fit.types import Type


class DynamicField(Type):
    def __init__(self, base, **kwargs):
        super(DynamicField, self).__init__(base.number)

        self.base = base
        self.referred = kwargs.keys()[0]
        self.variants = kwargs[self.referred] or {}

    def __repr__(self):
        return '<%s of %r>' % (
            self.__class__.__name__, self.base
        )

    @property
    def type(self):
        return self.base.type

    def read(self, read_buffer, architecture="<"):
        return self.base.read(read_buffer, architecture=architecture)

    def write(self, value):
        return self.base.write(value)

    def get_subfield(self, referred_value):
        for keys, subfield in self.variants.items():
            if not isinstance(keys, (list, tuple, set, frozenset)):
                keys = (keys,)
            if referred_value in keys:
                return subfield

        return None


class SubField(object):
    def __init__(self, field_name, field_type=None, **kwargs):
        self.name = field_name
        self.type = field_type
        self.kwargs = kwargs
