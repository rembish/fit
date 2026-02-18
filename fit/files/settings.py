"""Module docstring."""

from __future__ import annotations

from fit.files.device import DeviceFile
from fit.files.filelike import FileLike
from fit.messages.common import FileId
from fit.messages.settings import BikeProfile, HrmProfile, SdmProfile, UserProfile


class SettingsFile(FileLike):
    type = 2
    record_types = frozenset(
        (FileId, UserProfile, HrmProfile, SdmProfile, BikeProfile, DeviceFile)
    )
