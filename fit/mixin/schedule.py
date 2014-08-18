from fit.message.common import FileId
from fit.message.schedule import Schedule
from fit.mixin import FileMixin


class ScheduleFile(FileMixin):
    file_type = 7
    record_types = frozenset((FileId, Schedule))
