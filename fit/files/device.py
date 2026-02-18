"""Module docstring."""

from __future__ import annotations

from fit.files.filelike import FileLike
from fit.messages.common import FileId
from fit.messages.device import (
    Capabilities,
    FieldCapabilities,
    FileCapabilities,
    MesgCapabilities,
    Software,
)


class DeviceFile(FileLike):
    type = 1
    record_types = frozenset(
        (
            FileId,
            Software,
            Capabilities,
            FileCapabilities,
            MesgCapabilities,
            FieldCapabilities,
        )
    )
