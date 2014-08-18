from fit.message.common import FileId
from fit.message.sport_settings import ZonesTarget, Sport, HrZone, PowerZone, \
    MetZone, SpeedZone, CadenceZone
from fit.mixin import FileMixin


class SportSettingsFile(FileMixin):
    type = 3
    record_types = frozenset((
        FileId, ZonesTarget, Sport,
        HrZone, PowerZone, MetZone,
        SpeedZone, CadenceZone
    ))
