from fit.messages.common import FileId
from fit.messages.goals import Goal
from fit.files import FileLike


class GoalsFile(FileLike):
    type = 11
    record_types = frozenset((FileId, Goal))
