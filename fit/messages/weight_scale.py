from fit.messages import Message
from fit.types.additional import UPercents, Mass, Met, Years
from fit.types.extended import DateTime, Weight, MessageIndex
from fit.types.general import UInt8


class WeightScale(Message):
    msg_type = 30

    timestamp = DateTime(243)
    weight = Weight(0)
    percent_fat = UPercents(1)
    percent_hydration = UPercents(2)
    visceral_fat_mass = Mass(3)
    bone_mass = Mass(4)
    muscle_mass = Mass(5)
    basal_met = Met(7)
    physical_rating = UInt8(8)
    active_met = Met(9)
    metabolic_age = Years(10)
    visceral_fat_rating = UInt8(11)
    user_profile_index = MessageIndex(12)
