from fit.messages.activity import DeviceInfo
from fit.messages.blood_pressure import BloodPressure
from fit.messages.common import FileId
from fit.messages.settings import UserProfile
from fit.files import FileMixin


class BloodPressureFile(FileMixin):
    type = 14
    record_types = frozenset((FileId, UserProfile, BloodPressure, DeviceInfo))
