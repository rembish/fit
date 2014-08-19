from fit.message import Message
from fit.types.additional import HeartRate, Power, Speed, Cadence, MetCalories, \
    MetFatCalories
from fit.types.extended import SubSport, MessageIndex, HrZoneCalc, PwrZoneCalc
from fit.types.extended import Sport as SportField
from fit.types.general import String


class ZonesTarget(Message):
    msg_type = 7
    
    max_heart_rate = HeartRate(1)
    threshold_heart_rate = HeartRate(2)
    functional_threshold_power = Power(3)
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
    high_bpm = HeartRate(1)
    name = String(2)


class SpeedZone(Message):
    msg_type = 53

    message_index = MessageIndex(254)
    high_value = Speed(0)
    name = String(1)


class CadenceZone(Message):
    msg_type = 131

    message_index = MessageIndex(254)
    high_value = Cadence(0)
    name = String(1)


class PowerZone(Message):
    msg_type = 9

    message_index = MessageIndex(254)
    high_value = Power(1)
    name = String(2)


class MetZone(Message):
    msg_type = 10

    message_index = MessageIndex(254)
    high_bpm = HeartRate(1)
    calories = MetCalories(2)
    fat_calories = MetFatCalories(2)
