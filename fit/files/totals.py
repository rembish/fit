from fit.messages.common import FileId
from fit.messages.totals import Totals
from fit.files import FileMixin


class TotalsFile(FileMixin):
    type = 10
    record_types = frozenset((FileId, Totals))
