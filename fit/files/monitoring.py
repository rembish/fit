from fit.messages.activity import DeviceInfo
from fit.messages.common import FileId
from fit.messages.monitoring import MonitoringInfo, Monitoring
from fit.files import FileMixin


class MonitoringFile(FileMixin):
    record_types = frozenset((FileId, MonitoringInfo, Monitoring, DeviceInfo))


class MonitoringAFile(MonitoringFile):
    type = 15


class MonitoringBFile(MonitoringFile):
    type = 32


class DailyMonitoringFile(MonitoringFile):
    type = 28
