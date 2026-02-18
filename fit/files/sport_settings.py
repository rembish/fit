"""Module docstring."""

from __future__ import annotations

from fit.files.filelike import FileLike
from fit.messages.common import FileId
from fit.messages.sport_settings import (
    CadenceZone,
    HrZone,
    MetZone,
    PowerZone,
    SpeedZone,
    Sport,
    ZonesTarget,
)


class SportSettingsFile(FileLike):
    type = 3
    record_types = frozenset(
        (FileId, ZonesTarget, Sport, HrZone, PowerZone, MetZone, SpeedZone, CadenceZone)
    )
