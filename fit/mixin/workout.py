from fit.message.common import FileId
from fit.message.workout import Workout, WorkoutStep
from fit.mixin import FileMixin


class WorkoutFile(FileMixin):
    file_type = 5
    record_types = frozenset((FileId, Workout, WorkoutStep))
