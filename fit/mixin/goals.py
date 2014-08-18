from fit.message.common import FileId
from fit.message.goals import Goal
from fit.mixin import FileMixin


class GoalsFile(FileMixin):
    type = 11
    record_types = frozenset((FileId, Goal))
