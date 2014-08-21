from fit.messages.common import FileId
from fit.messages.device import Software, Capabilities, FileCapabilities, \
    MesgCapabilities, FieldCapabilities
from fit.files import FileMixin


class DeviceFile(FileMixin):
    type = 1
    record_types = frozenset((
        FileId, Software,
        Capabilities, FileCapabilities,
        MesgCapabilities, FieldCapabilities
    ))
