"""Module docstring."""

from __future__ import annotations

from fit.files.filelike import FileLike
from fit.messages.common import FileId
from fit.messages.totals import Totals


class TotalsFile(FileLike):
    type = 10
    record_types = frozenset((FileId, Totals))
