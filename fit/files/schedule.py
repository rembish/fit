from fit.messages.common import FileId
from fit.messages.schedule import Schedule
from fit.files import FileLike


class ScheduleFile(FileLike):
    type = 7
    record_types = frozenset((FileId, Schedule))
