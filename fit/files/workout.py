"""Module docstring."""

from __future__ import annotations

from fit.files.filelike import FileLike
from fit.messages.common import FileId
from fit.messages.workout import Workout, WorkoutStep


class WorkoutFile(FileLike):
    type = 5
    record_types = frozenset((FileId, Workout, WorkoutStep))
