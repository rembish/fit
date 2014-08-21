from fit.messages.activity import DeviceInfo
from fit.messages.common import FileId
from fit.messages.settings import UserProfile
from fit.messages.weight_scale import WeightScale
from fit.files import FileMixin


class WeightFile(FileMixin):
    type = 9
    record_types = frozenset((FileId, UserProfile, WeightScale, DeviceInfo))
