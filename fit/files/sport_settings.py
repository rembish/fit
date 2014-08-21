from fit.messages.common import FileId
from fit.messages.sport_settings import ZonesTarget, Sport, HrZone, PowerZone, \
    MetZone, SpeedZone, CadenceZone
from fit.files import FileMixin


class SportSettingsFile(FileMixin):
    type = 3
    record_types = frozenset((
        FileId, ZonesTarget, Sport,
        HrZone, PowerZone, MetZone,
        SpeedZone, CadenceZone
    ))
