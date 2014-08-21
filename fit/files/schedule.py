from fit.messages.common import FileId
from fit.messages.schedule import Schedule
from fit.files import FileMixin


class ScheduleFile(FileMixin):
    type = 7
    record_types = frozenset((FileId, Schedule))
