# coding=utf-8
from fit.messages import Message
from fit.types.dynamic import DynamicField, SubField
from fit.types.general import UInt32Z, UInt16, UInt32, UInt8, SInt16, SInt8, \
    String, Byte, UInt8Z, UInt16Z, SInt32
from fit.types.extended import DateTime, Manufacturer, LocalDateTime, \
    EventType, MessageIndex, LeftRightBalance100, LeftRightBalance, Sport, \
    SubSport, SessionTrigger, SwimStroke, DisplayMeasure, Intensity, \
    LapTrigger, LengthType, ActivityType, StrokeType, DeviceIndex, \
    BatteryStatus, BodyLocation, AntNetwork, SourceType, TimerTrigger, \
    AntplusDeviceType, FitnessEquipmentState
from fit.types.extended import Activity as ActivityField, Event as EventField
from fit.types.helpers import degrees


class Activity(Message):
    msg_type = 34

    timestamp = DateTime(253)
    total_timer_time = UInt32(0, units="s") * 1000
    num_sessions = UInt16(1)
    type = ActivityField(2)
    event = EventField(3)
    event_type = EventType(4)
    local_timestamp = LocalDateTime(5)
    event_group = UInt8(6)


class Session(Message):
    msg_type = 18

    message_index = MessageIndex(254)
    timestamp = DateTime(253)
    event = EventField(0)
    event_type = EventType(1)
    start_time = DateTime(2)
    start_position_lat = degrees(3)
    start_position_long = degrees(4)
    sport = Sport(5)
    sub_sport = SubSport(6)
    total_elapsed_time = UInt32(7, units="s") * 1000
    total_timer_time = UInt32(8, units="s") * 1000
    total_distance = UInt32(9, units="m") * 100
    total_cycles = DynamicField(
        UInt32(10, units="cycles"),
        sport={
            "running": SubField("total_strides", units="strides")
        }
    )
    total_calories = UInt16(11) * "kcal"
    total_fat_calories = UInt16(13) * "kcal"
    avg_speed = UInt16(14, units="m/s") * 1000
    max_speed = UInt16(15, units="m/s") * 1000
    avg_heart_rate = UInt8(16) * "bpm"
    max_heart_rate = UInt8(17) * "bpm"
    avg_cadence = DynamicField(
        UInt8(18, units="rpm"),
        sport={
            "running": SubField("avg_running_cadence", units="strides/min")
        }
    )
    max_cadence = DynamicField(
        UInt8(19, units="rpm"),
        sport={
            "running": SubField("max_running_cadence", units="strides/min")
        }
    )
    avg_power = UInt16(20) * "watts"
    max_power = UInt16(21) * "watts"
    total_ascent = UInt16(22) * "m"
    total_descent = UInt16(23) * "m"
    total_training_effect = UInt8(24) * 10
    first_lap_index = UInt16(25)
    num_laps = UInt16(26)
    event_group = UInt8(27)
    trigger = SessionTrigger(28)
    nec_lat = degrees(29)
    nec_long = degrees(30)
    swc_lat = degrees(31)
    swc_long = degrees(32)
    normalized_power = UInt16(34) * "watts"
    training_stress_score = UInt16(35, units="tss") * 10
    intensity_factor = UInt16(36, units="if") * 1000
    left_right_balance = LeftRightBalance100(37)
    avg_stroke_count = UInt32(41, units="strokes/lap") * 10
    avg_stroke_distance = UInt16(42, units="m") * 100
    swim_stroke = SwimStroke(43)
    pool_length = UInt16(44, units="m") * 100
    pool_length_unit = DisplayMeasure(46)
    num_active_lengths = UInt16(47)
    total_work = UInt32(48) * "J"
    avg_altitude = UInt16(49, units="m") * 5 + 500
    max_altitude = UInt16(50, units="m") * 5 + 500
    gps_accuracy = UInt8(51) * "m"
    avg_grade = SInt16(52, units="%") * 100
    avg_pos_grade = SInt16(53, units="%") * 100
    avg_neg_grade = SInt16(54, units="%") * 100
    max_pos_grade = SInt16(55, units="%") * 100
    max_neg_grade = SInt16(56, units="%") * 100
    avg_temperature = SInt8(57) * "°C"
    max_temperature = SInt8(58) * "°C"
    total_moving_time = UInt32(59, units="s") * 1000
    avg_pos_vertical_speed = SInt16(60, units="m/s") * 1000
    avg_neg_vertical_speed = SInt16(61, units="m/s") * 1000
    max_pos_vertical_speed = SInt16(62, units="m/s") * 1000
    max_neg_vertical_speed = SInt16(63, units="m/s") * 1000
    min_heart_rate = UInt8(64) * "bpm"
    time_in_hr_zone = UInt32(65, units="s") * 1000  # array
    time_in_speed_zone = UInt32(66, units="s") * 1000  # array
    time_in_cadence_zone = UInt32(67, units="s") * 1000  # array
    time_in_power_zone = UInt32(68, units="s") * 1000  # array
    avg_lap_time = UInt32(69, units="s") * 1000
    best_lap_index = UInt16(70)
    min_altitude = UInt16(71, units="m") * 5 + 500
    player_score = UInt16(82)
    opponent_score = UInt16(83)
    opponent_name = String(84)
    stroke_count = UInt16(85)  # array
    zone_count = UInt16(86)  # array
    max_ball_speed = UInt16(87, units="m/s") * 100
    avg_ball_speed = UInt16(88, units="m/s") * 100
    avg_vertical_oscillation = UInt16(89, units="mm") * 10
    avg_stance_time_percent = UInt16(90, units="%") * 100
    avg_stance_time = UInt16(91, units="ms") * 10
    avg_fractional_cadence = UInt8(92, units="rpm") * 128
    max_fractional_cadence = UInt8(93, units="rpm") * 128
    total_fractional_cycles = UInt8(94, units="cycles") * 128
    avg_total_hemoglobin_conc = UInt16(95, units="g/dL") * 100  # array
    min_total_hemoglobin_conc = UInt16(96, units="g/dL") * 100  # array
    max_total_hemoglobin_conc = UInt16(97, units="g/dL") * 100  # array
    avg_saturated_hemoglobin_percent = UInt16(98, units="%") * 10  # array
    min_saturated_hemoglobin_percent = UInt16(99, units="%") * 10  # array
    max_saturated_hemoglobin_percent = UInt16(100, units="%") * 10  # array
    avg_left_torque_effectiveness = UInt8(101, units="%") * 2
    avg_right_torque_effectiveness = UInt8(102, units="%") * 2
    avg_left_pedal_smoothness = UInt8(103, units="%") * 2
    avg_right_pedal_smoothness = UInt8(104, units="%") * 2
    avg_combined_pedal_smoothness = UInt8(105, units="%") * 2


class Lap(Message):
    msg_type = 19

    message_index = MessageIndex(254)
    timestamp = DateTime(253)
    event = EventField(0)
    event_type = EventType(1)
    start_time = DateTime(2)
    start_position_lat = degrees(3)
    start_position_long = degrees(4)
    end_position_lat = degrees(5)
    end_position_long = degrees(6)
    total_elapsed_time = UInt32(7, units="s") * 1000
    total_timer_time = UInt32(8, units="s") * 1000
    total_distance = UInt32(9, units="m") * 100
    total_cycles = DynamicField(
        UInt32(10, units="cycles"),
        sport={
            "running": SubField("total_strides", units="strides")
        }
    )
    total_calories = UInt16(11) * "kcal"
    total_fat_calories = UInt16(12) * "kcal"
    avg_speed = UInt16(13, units="m/s") * 1000
    max_speed = UInt16(14, units="m/s") * 1000
    avg_heart_rate = UInt8(15) * "bpm"
    max_heart_rate = UInt8(16) * "bpm"
    avg_cadence = DynamicField(
        UInt8(17, units="rpm"),
        sport={
            "running": SubField("avg_running_cadence", units="strides/min")
        }
    )
    max_cadence = DynamicField(
        UInt8(18, units="rpc"),
        sport={
            "running": SubField("max_running_cadence", units="strides/min")
        }
    )
    avg_power = UInt16(19) * "watts"
    max_power = UInt16(20) * "watts"
    total_ascent = UInt16(21) * "m"
    total_descent = UInt16(22) * "m"
    intensity = Intensity(23)
    lap_trigger = LapTrigger(24)
    sport = Sport(25)
    event_group = UInt8(26)
    num_lengths = UInt16(32)
    normalized_power = UInt16(33) * "watts"
    left_right_balance = LeftRightBalance100(34)
    first_length_index = UInt16(35)
    avg_stroke_distance = UInt16(37, units="m") * 100
    swim_stroke = SwimStroke(38)
    sub_sport = SubSport(39)
    num_active_lengths = UInt16(40)
    total_work = UInt32(41) * "J"
    avg_altitude = UInt16(42, units="m") * 5 + 500
    max_altitude = UInt16(43, units="m") * 5 + 500
    gps_accuracy = UInt8(44) * "m"
    avg_grade = SInt16(45, units="%") * 100
    avg_pos_grade = SInt16(46, units="%") * 100
    avg_neg_grade = SInt16(47, units="%") * 100
    max_pos_grade = SInt16(48, units="%") * 100
    max_neg_grade = SInt16(49, units="%") * 100
    avg_temperature = SInt8(50) * "°C"
    max_temperature = SInt8(51) * "°C"
    total_moving_time = UInt32(52, units="s") * 1000
    avg_pos_vertical_speed = SInt16(53, units="m/s") * 1000
    avg_neg_vertical_speed = SInt16(54, units="m/s") * 1000
    max_pos_vertical_speed = SInt16(55, units="m/s") * 1000
    max_neg_vertical_speed = SInt16(56, units="m/s") * 1000
    time_in_hr_zone = UInt32(57, units="s") * 1000  # array
    time_in_speed_zone = UInt32(58, units="s") * 1000  # array
    time_in_cadence_zone = UInt32(59, units="s") * 1000  # array
    time_in_power_zone = UInt32(60, units="s") * 1000  # array
    repetition_num = UInt16(61)
    min_altitude = UInt16(62, units="m") * 5 + 500
    min_heart_rate = UInt8(63) * "bpm"
    wkt_step_index = MessageIndex(71)
    opponent_score = UInt16(74)
    stroke_count = UInt16(75)  # array
    zone_count = UInt16(76)  # array
    avg_vertical_oscillation = UInt16(77, units="mm") * 10
    avg_stance_time_percent = UInt16(78, units="%") * 100
    avg_stance_time = UInt16(79, units="ms") * 10
    avg_fractional_cadence = UInt8(80, units="rpm") * 128
    max_fractional_cadence = UInt8(81, units="rpm") * 128
    total_fractional_cycles = UInt8(82, units="cycles") * 128
    player_score = UInt16(83)
    avg_total_hemoglobin_conc = UInt16(84, units="g/dL") * 100  # array
    min_total_hemoglobin_conc = UInt16(85, units="g/dL") * 100  # array
    max_total_hemoglobin_conc = UInt16(86, units="g/dL") * 100  # array
    avg_saturated_hemoglobin_percent = UInt16(87, units="%") * 10  # array
    min_saturated_hemoglobin_percent = UInt16(88, units="%") * 10  # array
    max_saturated_hemoglobin_percent = UInt16(89, units="%") * 10  # array
    avg_left_torque_effectiveness = UInt8(91, units="%") * 2
    avg_right_torque_effectiveness = UInt8(92, units="%") * 2
    avg_left_pedal_smoothness = UInt8(93, units="%") * 2
    avg_right_pedal_smoothness = UInt8(94, units="%") * 2
    avg_combined_pedal_smoothness = UInt8(95, units="%") * 2


class Length(Message):
    msg_type = 101

    message_index = MessageIndex(254)
    timestamp = DateTime(253)
    event = EventField(0)
    event_type = EventType(1)
    start_time = DateTime(2)
    total_elapsed_time = UInt32(3, units="s") * 1000
    total_timer_time = UInt32(4, units="s") * 1000
    total_strokes = UInt16(5) * "strokes"
    avg_speed = UInt16(6, units="m/s") * 1000
    swim_stroke = SwimStroke(7)
    avg_swimming_cadence = UInt8(9) * "strokes/min"
    event_group = UInt8(10)
    total_calories = UInt16(11) * "kcal"
    length_type = LengthType(12)
    player_score = UInt16(18)
    opponent_score = UInt16(19)
    stroke_count = UInt16(20)  # array
    zone_count = UInt16(21)  # array


class Record(Message):
    msg_type = 20

    timestamp = DateTime(253)
    position_lat = degrees(0)
    position_long = degrees(1)
    altitude = UInt16(2, units="m") * 5 + 500
    heart_rate = UInt8(3) * "bpm"
    cadence = UInt8(4) * "rpm"
    distance = UInt32(5, units="m") * 100
    speed = UInt16(6, units="m/s") * 1000
    power = UInt16(7) * "watts"
    compressed_speed_distance = Byte(8, count=3)  # components
    grade = SInt16(9, units="%") * 100
    resistance = UInt8(10)
    time_from_course = SInt32(11, units="s") * 1000
    cycle_length = UInt8(12, units="m") * 100
    temperature = SInt8(13) * "°C"
    speed_1s = UInt8(17, units="m/s") * 16  # array
    cycles = UInt8(18) * "cycles"  # components
    total_cycles = UInt32(19) * "cycles"
    compressed_accumulated_power = UInt16(28) * "watts"  # components
    accumulated_power = UInt32(29) * "watts"
    left_right_balance = LeftRightBalance(30)
    gps_accuracy = UInt8(31) * "m"
    vertical_speed = SInt16(32, units="m/s") * 1000
    calories = UInt16(33) * "kcal"
    vertical_oscillation = UInt16(39, units="mm") * 10
    stance_time_percent = UInt16(40, units="%") * 100
    stance_time = UInt16(41, units="ms") * 10
    activity_type = ActivityType(42)
    left_torque_effectiveness = UInt8(43, units="%") * 2
    right_torque_effectiveness = UInt8(44, units="%") * 2
    left_pedal_smoothness = UInt8(45, units="%") * 2
    right_pedal_smoothness = UInt8(46, units="%") * 2
    combined_pedal_smoothness = UInt8(47, units="%") * 2
    time128 = UInt8(48, units="s") * 128
    stroke_type = StrokeType(49)
    zone = UInt8(50)
    ball_speed = UInt16(51, units="m/s") * 100
    cadence256 = UInt16(52, units="rpm") * 256
    total_hemoglobin_conc = UInt16(54, units="g/dL") * 100
    total_hemoglobin_conc_min = UInt16(55, units="g/dL") * 100
    total_hemoglobin_conc_max = UInt16(56, units="g/dL") * 100
    saturated_hemoglobin_percent = UInt16(57, units="%") * 10
    saturated_hemoglobin_percent_min = UInt16(58, units="%") * 10
    saturated_hemoglobin_percent_max = UInt16(59, units="%") * 10
    device_index = DeviceIndex(62)


class Event(Message):
    msg_type = 21

    timestamp = DateTime(253)
    event = EventField(0)
    event_type = EventType(1)
    data16 = UInt16(2)  # components
    data = DynamicField(
        UInt32(3),
        event={
            "timer": SubField("timer_trigger", TimerTrigger),
            "course_point": SubField("course_point_index", MessageIndex),
            "battery": SubField(
                "battery_level",
                lambda number: UInt16(number, units="V") * 1000),
            "virtual_partner_pace": SubField(
                "virtual_partner_speed",
                lambda number: UInt16(number, units="m/s") * 1000),
            "hr_high_alert": SubField("hr_high_alert", UInt8, units="bpm"),
            "hr_low_alert": SubField("hr_low_alert", UInt8, units="bpm"),
            "speed_high_alert": SubField(
                "speed_high_alert",
                lambda number: UInt16(number, units="m/s") * 1000),
            "speed_low_alert": SubField(
                "speed_low_alert",
                lambda number: UInt16(number, units="m/s") * 1000),
            "cad_high_alert": SubField("cad_high_alert", UInt16, units="rpm"),
            "cad_low_alert": SubField("cad_low_alert", UInt16, units="rpm"),
            "power_high_alert": SubField(
                "power_high_alert", UInt16, units="watts"),
            "power_low_alert": SubField(
                "power_low_alert", UInt16, units="watts"),
            "time_duration_alert": SubField(
                "time_duration_alert",
                lambda number: UInt32(number, units="s") * 1000),
            "distance_duration_alert": SubField(
                "distance_duration_alert",
                lambda number: UInt32(number, units="m") * 100),
            "calorie_duration_alert": SubField(
                "calorie_duration_alert", units="calories"),
            "fitness_equipment": SubField(
                "fitness_equipment_state", FitnessEquipmentState),
            "sport_point": SubField("sport_point"),  # components
            ("front_gear_change", "rear_gear_change"): SubField(
                "gear_change_data")  # components
        }
    )
    event_group = UInt8(4)
    score = UInt16(7)
    opponent_score = UInt16(8)
    front_gear_num = UInt8Z(9)
    front_gear = UInt8Z(10)
    rear_gear_num = UInt8Z(11)
    rear_gear = UInt8Z(12)


class DeviceInfo(Message):
    msg_type = 23

    timestamp = DateTime(253)
    device_index = DeviceIndex(0)
    device_type = DynamicField(
        UInt8(1),
        source_type={
            "antplus": SubField("antplus_device_type", AntplusDeviceType),
            "ant": SubField("ant_device_type")
        }
    )
    manufacturer = Manufacturer(2)
    serial_number = UInt32Z(3)
    product = UInt16(4)  # Maybe DynamicField?
    software_version = UInt16(5) * 100
    hardware_version = UInt8(6)
    cum_operating_time = UInt32(7) * "s"
    battery_voltage = UInt16(10, units="V") * 256
    battery_status = BatteryStatus(11)
    sensor_position = BodyLocation(18)
    descriptor = String(19)
    ant_transmission_type = UInt8Z(20)
    ant_device_number = UInt16Z(21)
    ant_network = AntNetwork(22)
    source_type = SourceType(25)


class Hrv(Message):
    msg_type = 78

    time = UInt16(0, units="s") * 1000  # array
