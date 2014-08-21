from fit.messages.activity import Lap, Record
from fit.messages.common import FileId
from fit.messages.course import Course, CoursePoint
from fit.files import FileLike


class ActivitySummaryFile(FileLike):
    type = 6
    record_types = frozenset((FileId, Course, CoursePoint, Lap, Record))
