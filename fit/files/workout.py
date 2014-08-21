from fit.messages.common import FileId
from fit.messages.workout import Workout, WorkoutStep
from fit.files import FileMixin


class WorkoutFile(FileMixin):
    type = 5
    record_types = frozenset((FileId, Workout, WorkoutStep))
