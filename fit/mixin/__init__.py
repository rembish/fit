from fit.message import Message
from fit.message.common import FileId
from fit.utils import get_known


class FileMixin(object):
    type = None
    record_types = frozenset((Message,))

    @classmethod
    def create(cls, filename, mixin=None):
        from fit import FitFile

        instance = FitFile.open(filename, mode='w')

        mixin = mixin or cls
        if not mixin:
            return instance

        if isinstance(mixin, int):
            mixin = KNOWN[mixin]

        instance.append(FileId.create(mixin.type))
        return instance

    def _apply_mixin(self):
        from fit import FitFile

        mcs = [FitFile]
        if self.body.file_id:
            mixin_cls = KNOWN.get(self.body.file_id.filetype)
            if mixin_cls:
                mcs.append(mixin_cls)
        self.__class__ = type(mcs[-1].__name__, tuple(mcs), {})

    def _validate(self, i, value=None):
        if not value:  # removing
            if i == 0 and len(self.body) > 1 and self.body.file_id:
                raise IndexError(
                    "Can't remove file id record from not empty file")
        else:  # inserting or updating
            if i == 0 and len(self.body) > 1 and self.body.file_id:
                raise IndexError(
                    "Can't update file id record of not empty file")
            elif not isinstance(value, tuple(self.record_types)):
                raise TypeError("%s doesn't support %s records" % (
                    self.__class__.__name__, value.__class__.__name__))


KNOWN = get_known(__name__, FileMixin)
