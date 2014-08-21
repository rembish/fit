from fit.messages.activity import Activity, Session, Lap, Length, Record, \
    Event, DeviceInfo, Hrv
from fit.messages.common import FileId
from fit.files import FileLike


class ActivityFile(FileLike):
    type = 4
    record_types = frozenset((
        FileId, Activity, Session, Lap, Length, Record, Event, DeviceInfo, Hrv
    ))
