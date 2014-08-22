from fit.types import Type


class Dynamic(Type):
    def __init__(self, base, **kwargs):
        super(Dynamic, self).__init__(base.number)

        self.base = base
        self.referred = kwargs.keys()[0]
        self.variants = kwargs[self.referred] or {}

    def read(self, read_buffer, architecture="<"):
        return self.base.read(read_buffer, architecture=architecture)

    def write(self, value):
        return self.base.write(value)

    def mutate(self, referred_value):
        for keys, field_cls in self.variants.items():
            if not isinstance(keys, (list, tuple, set, frozenset)):
                keys = (keys,)
            if referred_value in keys:
                return field_cls(self.number)

        return self.base
