from fit.messages.common import FileId
from fit.messages.settings import UserProfile, HrmProfile, SdmProfile, \
    BikeProfile
from fit.files import FileMixin
from fit.files.device import DeviceFile


class SettingsFile(FileMixin):
    type = 2
    record_types = frozenset((
        FileId, UserProfile, HrmProfile, SdmProfile, BikeProfile, DeviceFile
    ))
