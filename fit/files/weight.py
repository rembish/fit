"""Module docstring."""

from __future__ import annotations

from fit.files.filelike import FileLike
from fit.messages.activity import DeviceInfo
from fit.messages.common import FileId
from fit.messages.settings import UserProfile
from fit.messages.weight_scale import WeightScale


class WeightFile(FileLike):
    type = 9
    record_types = frozenset((FileId, UserProfile, WeightScale, DeviceInfo))
