from fit.messages.common import FileId
from fit.messages.goals import Goal
from fit.files import FileMixin


class GoalsFile(FileMixin):
    type = 11
    record_types = frozenset((FileId, Goal))
