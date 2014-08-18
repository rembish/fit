from fit.message.activity import DeviceInfo
from fit.message.common import FileId
from fit.message.monitoring import MonitoringInfo, Monitoring
from fit.mixin import FileMixin


class MonitoringFile(FileMixin):
    record_types = frozenset((FileId, MonitoringInfo, Monitoring, DeviceInfo))


class MonitoringAFile(MonitoringFile):
    file_type = 15


class MonitoringBFile(MonitoringFile):
    file_type = 32


class DailyMonitoringFile(MonitoringFile):
    file_type = 28
