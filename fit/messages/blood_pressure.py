from fit.messages import Message
from fit.types.extended import DateTime, MessageIndex, HrType, BpStatus
from fit.types.general import UInt16, UInt8


class BloodPressure(Message):
    msg_type = 51

    timestamp = DateTime(253)
    systolic_pressure = UInt16(0) * "mmHg"
    diastolic_pressure = UInt16(1) * "mmHg"
    mean_arterial_pressure = UInt16(2) * "mmHg"
    map_3_sample_mean = UInt16(3) * "mmHg"
    map_morning_values = UInt16(4) * "mmHg"
    map_evening_values = UInt16(5) * "mmHg"
    heart_rate = UInt8(6) * "bpm"
    heart_rate_type = HrType(7)
    status = BpStatus(8)
    user_profile_index = MessageIndex(9)
