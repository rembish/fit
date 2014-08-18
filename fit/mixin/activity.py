from fit.message.activity import Activity, Session, Lap, Length, Record, \
    Event, DeviceInfo, Hrv
from fit.message.common import FileId
from fit.mixin import FileMixin


class ActivityFile(FileMixin):
    file_type = 4
    record_types = frozenset((
        FileId, Activity, Session, Lap, Length, Record, Event, DeviceInfo, Hrv
    ))
