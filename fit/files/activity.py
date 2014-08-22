from fit.files import FileLike
from fit.messages.activity import Activity, Session, Lap, Length, Record, \
    Event, DeviceInfo, Hrv
from fit.messages.common import FileId, FileCreator
from fit.messages.course import Course, CoursePoint


class ActivityFile(FileLike):
    type = 4
    record_types = frozenset((
        FileId, FileCreator, Activity, Session, Lap, Length, Record, Event,
        DeviceInfo, Hrv
    ))


class ActivitySummaryFile(FileLike):
    type = 6
    record_types = frozenset((FileId, Course, CoursePoint, Lap, Record))
