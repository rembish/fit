from fit.messages.common import FileId
from fit.messages.settings import UserProfile, HrmProfile, SdmProfile, \
    BikeProfile
from fit.files import FileLike
from fit.files.device import DeviceFile


class SettingsFile(FileLike):
    type = 2
    record_types = frozenset((
        FileId, UserProfile, HrmProfile, SdmProfile, BikeProfile, DeviceFile
    ))
