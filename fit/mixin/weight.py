from fit.message.activity import DeviceInfo
from fit.message.common import FileId
from fit.message.settings import UserProfile
from fit.message.weight_scale import WeightScale
from fit.mixin import FileMixin


class WeightFile(FileMixin):
    type = 9
    record_types = frozenset((FileId, UserProfile, WeightScale, DeviceInfo))
