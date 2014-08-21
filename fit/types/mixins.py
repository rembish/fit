class KnownMixin(object):
    known = {}

    def _load(self, data):
        return self.known.get(data, data)

    def _save(self, value):
        for key, other in self.known.items():
            if value == other:
                return key
        return value


class ScaleMixin(object):
    scale = None
    offset = None

    def _load(self, data):
        value = float(data)
        if self.scale:
            value /= float(self.scale)
        if self.offset:
            value -= float(self.offset)
        return value

    def _save(self, value):
        data = value
        if self.offset:
            data += self.offset
        if self.scale:
            data *= self.scale
        return int(data)
