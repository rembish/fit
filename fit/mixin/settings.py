from fit.message.common import FileId
from fit.message.settings import UserProfile, HrmProfile, SdmProfile, \
    BikeProfile
from fit.mixin import FileMixin
from fit.mixin.device import DeviceFile


class SettingsFile(FileMixin):
    type = 2
    record_types = frozenset((
        FileId, UserProfile, HrmProfile, SdmProfile, BikeProfile, DeviceFile
    ))
