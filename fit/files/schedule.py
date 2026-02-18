"""Module docstring."""

from __future__ import annotations

from fit.files.filelike import FileLike
from fit.messages.common import FileId
from fit.messages.schedule import Schedule


class ScheduleFile(FileLike):
    type = 7
    record_types = frozenset((FileId, Schedule))
