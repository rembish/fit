from fit.message.common import FileId
from fit.utils import get_known


class FileMixin(object):
    type = None
    record_types = frozenset((FileId,))


KNOWN = get_known(__name__, FileMixin)
