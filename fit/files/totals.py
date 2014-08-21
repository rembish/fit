from fit.messages.common import FileId
from fit.messages.totals import Totals
from fit.files import FileLike


class TotalsFile(FileLike):
    type = 10
    record_types = frozenset((FileId, Totals))
