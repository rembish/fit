from fit.messages import Message
from fit.types.extended import MessageIndex, DisplayMeasure, Bool, Sport, \
    SubSport, Gender, Language, DisplayHeart, DisplayPower, DisplayPosition, \
    ActivityClass, UserLocalId
from fit.types.general import UInt8, UInt32, SInt8, UInt16, String, Byte, \
    UInt16Z, UInt8Z


class DeviceSettings(Message):
    msg_type = 2

    active_time_zone = UInt8(0)
    utc_offset = UInt32(1)
    time_zone_offset = SInt8(5)  # array


class UserProfile(Message):
    msg_type = 3

    message_index = MessageIndex(254)
    friendly_name = String(0)
    gender = Gender(1)
    age = UInt8(2) * "years"
    height = UInt8(3)
    weight = UInt16(4)
    language = Language(5)
    elev_setting = DisplayMeasure(6)
    weight_settings = DisplayMeasure(7)
    resting_heart_rate = UInt8(8) * "bpm"
    default_max_running_heart_rate = UInt8(9) * "bpm"
    default_max_biking_heart_rate = UInt8(10) * "bpm"
    default_max_heart_rate = UInt8(11) * "bpm"
    hr_setting = DisplayHeart(12)
    speed_setting = DisplayMeasure(13)
    dist_setting = DisplayMeasure(14)
    power_settings = DisplayPower(16)
    activity_class = ActivityClass(17)
    position_setting = DisplayPosition(18)
    temperature_setting = DisplayMeasure(21)
    local_id = UserLocalId(22)
    global_id = Byte(23)  # array
    height_setting = DisplayMeasure(30)


class HrmProfile(Message):
    msg_type = 4

    message_index = MessageIndex(254)
    enabled = Bool(0)
    hrm_ant_id = UInt16Z(1)
    log_hrv = Bool(2)
    hrm_ant_id_trans_type = UInt8Z(3)


class SdmProfile(Message):
    msg_type = 5

    message_index = MessageIndex(254)
    enabled = Bool(0)
    sdm_ant_id = UInt16Z(1)
    sdm_cal_factor = UInt16(2)
    odometer = UInt32(3, units="m") * 100
    speed_source = Bool(4)
    sdm_ant_id_trans_byte = UInt8Z(5)
    odometer_rollover = UInt8(7)


class BikeProfile(Message):
    msg_type = 6

    message_index = MessageIndex(254)
    name = String(0)
    sport = Sport(1)
    sub_sport = SubSport(2)
    odometer = UInt32(3, units="m") * 100
    bike_spd_ant_id = UInt16Z(4)
    bike_cad_ant_id = UInt16Z(5)
    bike_spdcad_ant_id = UInt16Z(6)
    bike_power_ant_id = UInt16Z(7)
    custom_wheelsize = UInt16(8)
    auto_wheelsize = UInt16(9)
    bike_wieght = UInt16(10)
    power_cal_factor = UInt16(11)
    auto_wheel_cal = Bool(12)
    auto_power_zero = Bool(13)
    id = UInt8(14)
    spd_enabled = Bool(15)
    cad_enabled = Bool(16)
    spdcad_enabled = Bool(17)
    power_enabled = Bool(18)
    crank_length = UInt8(19)
    enabled = Bool(20)
    bike_spd_ant_id_trans_type = UInt8Z(21)
    bike_cad_ant_id_trans_type = UInt8Z(22)
    bike_spdcad_ant_id_trans_type = UInt8Z(23)
    bike_power_ant_id_trans_type = UInt8Z(24)
    odometer_rollover = UInt8(37)
    front_gear_num = UInt8Z(38)
    front_gear = UInt8Z(39)
    rear_gear_num = UInt8Z(40)
    read_gear = UInt8Z(41)
