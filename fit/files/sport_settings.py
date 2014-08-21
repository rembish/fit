from fit.messages.common import FileId
from fit.messages.sport_settings import ZonesTarget, Sport, HrZone, PowerZone, \
    MetZone, SpeedZone, CadenceZone
from fit.files import FileLike


class SportSettingsFile(FileLike):
    type = 3
    record_types = frozenset((
        FileId, ZonesTarget, Sport,
        HrZone, PowerZone, MetZone,
        SpeedZone, CadenceZone
    ))
