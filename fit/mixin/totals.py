from fit.message.common import FileId
from fit.message.totals import Totals
from fit.mixin import FileMixin


class TotalsFile(FileMixin):
    file_type = 10
    record_types = frozenset((FileId, Totals))
