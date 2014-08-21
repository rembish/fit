from fit.messages.common import FileId
from fit.messages.workout import Workout, WorkoutStep
from fit.files import FileLike


class WorkoutFile(FileLike):
    type = 5
    record_types = frozenset((FileId, Workout, WorkoutStep))
