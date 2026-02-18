"""Module docstring."""

from __future__ import annotations

from fit.files.filelike import FileLike
from fit.messages.activity import (
    Activity,
    DeviceInfo,
    Event,
    Hrv,
    Lap,
    Length,
    Record,
    Session,
)
from fit.messages.common import FileCreator, FileId
from fit.messages.course import Course, CoursePoint


class ActivityFile(FileLike):
    type = 4
    record_types = frozenset(
        (
            FileId,
            FileCreator,
            Activity,
            Session,
            Lap,
            Length,
            Record,
            Event,
            DeviceInfo,
            Hrv,
        )
    )


class ActivitySummaryFile(FileLike):
    type = 6
    record_types = frozenset((FileId, Course, CoursePoint, Lap, Record))
