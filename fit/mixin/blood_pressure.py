from fit.message.activity import DeviceInfo
from fit.message.blood_pressure import BloodPressure
from fit.message.common import FileId
from fit.message.settings import UserProfile
from fit.mixin import FileMixin


class BloodPressureFile(FileMixin):
    type = 14
    record_types = frozenset((FileId, UserProfile, BloodPressure, DeviceInfo))
