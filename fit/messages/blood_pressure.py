from fit.messages import Message
from fit.types.additional import Pressure, HeartRate
from fit.types.extended import DateTime, MessageIndex, HrType, BpStatus


class BloodPressure(Message):
    msg_type = 51

    timestamp = DateTime(253)
    systolic_pressure = Pressure(0)
    diastolic_pressure = Pressure(1)
    mean_arterial_pressure = Pressure(2)
    map_3_sample_mean = Pressure(3)
    map_morning_values = Pressure(4)
    map_evening_values = Pressure(5)
    heart_rate = HeartRate(6)
    heart_rate_type = HrType(7)
    status = BpStatus(8)
    user_profile_index = MessageIndex(9)
