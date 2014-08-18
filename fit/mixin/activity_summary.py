from fit.message.activity import Lap, Record
from fit.message.common import FileId
from fit.message.course import Course, CoursePoint
from fit.mixin import FileMixin


class ActivitySummaryFile(FileMixin):
    type = 6
    record_types = frozenset((FileId, Course, CoursePoint, Lap, Record))
