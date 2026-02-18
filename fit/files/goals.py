"""Module docstring."""

from __future__ import annotations

from fit.files.filelike import FileLike
from fit.messages.common import FileId
from fit.messages.goals import Goal


class GoalsFile(FileLike):
    type = 11
    record_types = frozenset((FileId, Goal))
