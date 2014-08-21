from fit.messages.activity import Activity, Session, Lap, Length, Record, \
    Event, DeviceInfo, Hrv
from fit.messages.common import FileId
from fit.files import FileMixin


class ActivityFile(FileMixin):
    type = 4
    record_types = frozenset((
        FileId, Activity, Session, Lap, Length, Record, Event, DeviceInfo, Hrv
    ))
