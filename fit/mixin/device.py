from fit.message.common import FileId
from fit.message.device import Software, Capabilities, FileCapabilities, \
    MesgCapabilities, FieldCapabilities
from fit.mixin import FileMixin


class DeviceFile(FileMixin):
    file_type = 1
    record_types = frozenset((
        FileId, Software,
        Capabilities, FileCapabilities,
        MesgCapabilities, FieldCapabilities
    ))
