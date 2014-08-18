from fit.message.common import FileId
from fit.utils import get_known


class FileMixin(object):
    file_type = None
    record_types = frozenset((FileId,))


KNOWN = get_known(__name__, FileMixin, key="file_type")
