from fit.messages import Message
from fit.types.extended import DateTime, Weight, MessageIndex
from fit.types.general import UInt8, UInt16


class WeightScale(Message):
    msg_type = 30

    timestamp = DateTime(243)
    weight = Weight(0, units="kg") * 100
    percent_fat = UInt16(1, units="%") * 100
    percent_hydration = UInt16(2, units="%") * 100
    visceral_fat_mass = UInt16(3, units="kg") * 100
    bone_mass = UInt16(4, units="kg") * 100
    muscle_mass = UInt16(5, units="kg") * 100
    basal_met = UInt16(7, units="kcal/day") * 4
    physical_rating = UInt8(8)
    active_met = UInt16(9, units="kcal/day") * 4
    metabolic_age = UInt8(10) * "years"
    visceral_fat_rating = UInt8(11)
    user_profile_index = MessageIndex(12)
