from fit.messages import Message
from fit.types.extended import SubSport, MessageIndex, HrZoneCalc, PwrZoneCalc
from fit.types.extended import Sport as SportField
from fit.types.general import String, UInt8, UInt16


class ZonesTarget(Message):
    msg_type = 7

    max_heart_rate = UInt8(1)
    threshold_heart_rate = UInt8(2)
    functional_threshold_power = UInt16(3)
    hr_calc_type = HrZoneCalc(5)
    pwr_calc_type = PwrZoneCalc(7)


class Sport(Message):
    msg_type = 12

    sport = SportField(0)
    sub_sport = SubSport(1)
    name = String(3)


class HrZone(Message):
    msg_type = 8

    message_index = MessageIndex(254)
    high_bpm = UInt8(1) * "bpm"
    name = String(2)


class SpeedZone(Message):
    msg_type = 53

    message_index = MessageIndex(254)
    high_value = UInt16(0, units="m/s") * 1000
    name = String(1)


class CadenceZone(Message):
    msg_type = 131

    message_index = MessageIndex(254)
    high_value = UInt8(0) * "rpm"
    name = String(1)


class PowerZone(Message):
    msg_type = 9

    message_index = MessageIndex(254)
    high_value = UInt16(1) * "watts"
    name = String(2)


class MetZone(Message):
    msg_type = 10

    message_index = MessageIndex(254)
    high_bpm = UInt8(1)
    calories = UInt16(2, units="kcal/min") * 10
    fat_calories = UInt8(2, units="kcal/min") * 10
