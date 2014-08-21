from fit.messages import Message
from fit.types.additional import Calories, Distance, Cycles, TimerTime, \
    Temperature, HeartRate
from fit.types.extended import DateTime, LocalDateTime, ActivityType, \
    DeviceIndex, Intensity, ActivitySubType
from fit.types.general import UInt16, Byte, UInt8, UInt32


class MonitoringInfo(Message):
    msg_type = 103

    timestamp = DateTime(253)
    local_timestamp = LocalDateTime(0)
    activity_type = ActivityType(1)
    cycles_to_distance = UInt16(3)
    cycles_to_calories = UInt16(4)
    resting_metabolic_rate = UInt16(5)


class Monitoring(Message):
    msg_type = 55

    timestamp = DateTime(253)
    device_index = DeviceIndex(0)
    calories = Calories(1)
    distance = Distance(2)
    cycles = Cycles(3)
    active_time = TimerTime(4)
    activity_type = ActivityType(5)
    activity_subtime = ActivitySubType(6)
    activity_level = ActivityLevel(7)
    distance_16 = UInt16(8)
    cycles_16 = UInt16(9)
    active_time_16 = UInt16(10)
    local_timestamp = LocalDateTime(11)
    temperature = Temperature(12)
    temperature_min = Temperature(14)
    temperature_max = Temperature(15)
    activity_time = UInt16(16)
    active_calories = Calories(19)
    current_activity_type_intensity = Byte(24)
    timestamp_min_8 = UInt8(25)
    timestamp_16 = UInt16(26)
    heart_rate = HeartRate(27)
    intensity = Intensity(28)
    duration_min = UInt16(29)
    duration = UInt32(30)
