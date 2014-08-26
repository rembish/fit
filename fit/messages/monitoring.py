# coding=utf-8
from fit.messages import Message
from fit.types.dynamic import DynamicField, SubField
from fit.types.extended import DateTime, LocalDateTime, ActivityType, \
    DeviceIndex, Intensity, ActivitySubType, ActivityLevel
from fit.types.general import UInt16, Byte, UInt8, UInt32, SInt16


class MonitoringInfo(Message):
    msg_type = 103

    timestamp = DateTime(253)
    local_timestamp = LocalDateTime(0)
    activity_type = ActivityType(1)  # array
    cycles_to_distance = UInt16(3, units="m/cycle") * 5000  # array
    cycles_to_calories = UInt16(4, units="kcal/cycle") * 5000  # array
    resting_metabolic_rate = UInt16(5) * "kcal/day"


class Monitoring(Message):
    msg_type = 55

    timestamp = DateTime(253)
    device_index = DeviceIndex(0)
    calories = UInt16(1) * "kcal"
    distance = UInt32(2, units="m") * 100
    cycles = DynamicField(
        UInt32(3, units="cycles") * 2,
        activity_type={
            ("walking", "running"): SubField("steps", units="steps"),
            ("cycling", "swimming"): SubField(
                "strokes", lambda number: UInt32(number, units="strokes") * 2
            )
        }
    )
    active_time = UInt32(4, units="s") * 1000
    activity_type = ActivityType(5)
    activity_subtime = ActivitySubType(6)
    activity_level = ActivityLevel(7)
    distance_16 = UInt16(8)
    cycles_16 = UInt16(9)
    active_time_16 = UInt16(10)
    local_timestamp = LocalDateTime(11)
    temperature = SInt16(12, units="°C") * 100
    temperature_min = SInt16(14, units="°C") * 100
    temperature_max = SInt16(15, units="°C") * 100
    activity_time = UInt16(16) * "minutes"  # array
    active_calories = UInt16(19) * "kcal"
    current_activity_type_intensity = Byte(24)  # components
    timestamp_min_8 = UInt8(25) * "min"
    timestamp_16 = UInt16(26) * "s"
    heart_rate = UInt8(27) * "bpm"
    intensity = Intensity(28)
    duration_min = UInt16(29) * "min"
    duration = UInt32(30) * "s"
