from fit.messages import Message
from fit.types.additional import Altitude, Degrees, TimerTime, Distance, \
    Cycles, Calories, Speed, HeartRate, Cadence, Power, Difference, \
    StressScore, IntensityFactor, StrokeCount, Work, Percents, Temperature, \
    SSpeed, BallSpeed, Oscillation, StanceTime, FractionalCadence, \
    FractionalCycles, Hemoglobin, HemoglobinPercents, Accuracy, \
    StancePercents, Version
from fit.types.general import UInt32Z, UInt16, UInt32, UInt8, SInt16, SInt8, \
    String, Byte, UInt8Z, UInt16Z
from fit.types.extended import DateTime, Manufacturer, LocalDateTime, \
    EventType, MessageIndex, LeftRightBalance100, LeftRightBalance, Sport, \
    SubSport, SessionTrigger, SwimStroke, DisplayMeasure, Intensity, \
    LapTrigger, LengthType, ActivityType, StrokeType, DeviceIndex, \
    BatteryStatus, BodyLocation, AntNetwork, SourceType, Product
from fit.types.extended import Activity as ActivityField, Event as EventField


class Activity(Message):
    msg_type = 34

    timestamp = DateTime(253)
    total_timer_time = TimerTime(0)  # Exclude pauses
    local_timestamp = LocalDateTime(5)
    num_sessions = UInt16(1)
    type = ActivityField(2)
    event = EventField(3)
    event_type = EventType(4)
    event_group = UInt8(6)


class Session(Message):
    msg_type = 18

    timestamp = DateTime(253)  # Session end time
    start_time = DateTime(2)
    start_position_lat = Degrees(3)
    start_position_long = Degrees(4)
    total_elapsed_time = TimerTime(7)  # Time (includes pauses)
    total_timer_time = TimerTime(8)  # Time (excludes pauses)
    total_distance = Distance(9)
    total_cycles = Cycles(10)
    nec_lat = Degrees(29)
    nec_long = Degrees(30)
    swc_lat = Degrees(31)
    swc_long = Degrees(32)
    avg_stroke_count = StrokeCount(41)
    total_work = Work(48)
    total_moving_time = TimerTime(59)
    time_in_hr_zone = TimerTime(65)
    time_in_speed_zone = TimerTime(66)
    time_in_cadence_zone = TimerTime(67)
    time_in_power_zone = TimerTime(68)
    avg_lap_time = TimerTime(69)
    message_index = MessageIndex(254)  # Selected bit is set for the crrnt sess
    total_calories = Calories(11)
    total_fat_calories = Calories(13)
    avg_speed = Speed(14)  # total_distance / total_timer_time
    max_speed = Speed(15)
    avg_power = Power(20)
    max_power = Power(21)
    total_ascent = Difference(22)
    total_descent = Difference(23)
    first_lap_index = UInt16(25)
    num_laps = UInt16(26)
    normalized_power = Power(34)
    training_stress_score = StressScore(35)
    intensity_factor = IntensityFactor(36)
    left_right_balance = LeftRightBalance100(37)
    avg_stroke_distance = Distance(42)
    pool_length = Distance(44)
    num_active_lengths = UInt16(47)  # number of active lengths of swim pool
    avg_altitude = Altitude(49)
    max_altitude = Altitude(50)
    avg_grade = Percents(52)
    avg_pos_grade = Percents(53)
    avg_neg_grade = Percents(54)
    max_pos_grade = Percents(55)
    max_neg_grade = Percents(56)
    avg_pos_vertical_speed = SSpeed(60)
    avg_neg_vertical_speed = SSpeed(61)
    max_pos_vertical_speed = SSpeed(62)
    max_neg_vertical_speed = SSpeed(63)
    best_lap_index = UInt16(70)
    min_altitude = Altitude(71)
    player_score = UInt16(82)
    opponent_score = UInt16(83)
    stroke_count = UInt16(85)  # stroke_type enum used as the index
    zone_count = UInt16(86)  # zone number used as the index
    max_ball_speed = BallSpeed(87)
    avg_ball_speed = BallSpeed(88)
    avg_vertical_oscillation = Oscillation(89)
    avg_stance_time_percent = StancePercents(90)
    avg_stance_time = StanceTime(91)
    event = EventField(0)  # Session
    event_type = EventType(1)  # Stop
    sport = Sport(5)
    sub_sport = SubSport(6)
    avg_heart_rate = HeartRate(16)  # Average heart rate (excludes pause time)
    max_heart_rate = HeartRate(17)
    avg_cadence = Cadence(18)
    max_cadence = Cadence(19)
    total_training_effect = UInt8(24)
    event_group = UInt8(27)
    trigger = SessionTrigger(28)
    swim_stroke = SwimStroke(43)
    pool_length_unit = DisplayMeasure(46)
    gps_accuracy = Accuracy(51)
    avg_temperature = Temperature(57)
    max_temperature = Temperature(58)
    min_heart_rate = HeartRate(64)
    opponent_name = String(84)
    avg_fractional_cadence = FractionalCadence(92)
    max_fractional_cadence = FractionalCadence(93)
    total_fractional_cycles = FractionalCycles(94)


class Lap(Message):
    msg_type = 19

    timestamp = DateTime(253)
    start_time = DateTime(2)
    start_position_lat = Degrees(3)
    start_position_long = Degrees(4)
    end_position_lat = Degrees(5)
    end_position_long = Degrees(6)
    total_elapsed_time = TimerTime(7)
    total_timer_time = TimerTime(8)
    total_distance = Distance(9)
    total_cycles = UInt32(10)
    total_work = UInt32(41)
    total_moving_time = UInt32(52)
    time_in_hr_zone = UInt32(57)
    time_in_speed_zone = UInt32(58)
    time_in_cadence_zone = UInt32(59)
    time_in_power_zone = UInt32(60)
    message_index = MessageIndex(254)
    total_calories = UInt16(11)
    total_fat_calories = UInt16(12)
    avg_speed = UInt16(13)
    max_speed = Speed(14)
    avg_power = UInt16(19)
    max_power = UInt16(20)
    total_ascent = Difference(21)
    total_descent = Difference(22)
    num_lengths = UInt16(32)
    normalized_power = UInt16(33)
    left_right_balance = LeftRightBalance100(34)
    first_length_index = UInt16(35)
    avg_stroke_distance = UInt16(37)
    num_active_lengths = UInt16(40)
    avg_altitude = Altitude(42)
    max_altitude = Altitude(43)
    avg_grade = SInt16(45)
    avg_pos_grade = SInt16(46)
    avg_neg_grade = SInt16(47)
    max_pos_grade = SInt16(48)
    max_neg_grade = SInt16(49)
    avg_pos_vertical_speed = SInt16(53)
    avg_neg_vertical_speed = SInt16(54)
    max_pos_vertical_speed = SInt16(55)
    max_neg_vertical_speed = SInt16(56)
    repetition_num = UInt16(61)
    min_altitude = Altitude(62)
    wkt_step_index = MessageIndex(71)
    opponent_score = UInt16(74)
    stroke_count = UInt16(75)
    zone_count = UInt16(76)
    avg_vertical_oscillation = UInt16(77)
    avg_stance_time_percent = UInt16(78)
    avg_stance_time = UInt16(79)
    player_score = UInt16(83)
    avg_total_hemoglobin_conc = Hemoglobin(84)
    min_total_hemoglobin_conc = Hemoglobin(85)
    max_total_hemoglobin_conc = Hemoglobin(86)
    avg_saturated_hemoglobin_percent = HemoglobinPercents(87)
    min_saturated_hemoglobin_percent = HemoglobinPercents(88)
    max_saturated_hemoglobin_percent = HemoglobinPercents(89)
    event = EventField(0)
    event_type = EventType(1)
    avg_heart_rate = UInt8(15)
    max_heart_rate = UInt8(16)
    avg_cadence = UInt8(17)
    max_cadence = UInt8(18)
    intensity = Intensity(23)
    lap_trigger = LapTrigger(24)
    sport = Sport(25)
    EventGroup = UInt8(26)
    swim_stroke = SwimStroke(38)
    sub_sport = SubSport(39)
    gps_accuracy = UInt8(44)
    avg_temperature = SInt8(50)
    max_temperature = SInt8(51)
    min_heart_rate = UInt8(63)
    avg_fractional_cadence = UInt8(80)
    max_fractional_cadence = UInt8(81)
    total_fractional_cycles = UInt8(82)


class Length(Message):
    msg_type = 101

    timestamp = DateTime(253)
    start_time = DateTime(2)
    total_elapsed_time = UInt32(3)
    total_timer_time = UInt32(4)
    message_index = MessageIndex(254)
    total_strokes = UInt16(5)
    avg_speed = UInt16(6)
    total_calories = UInt16(11)
    player_score = UInt16(18)
    opponent_score = UInt16(19)
    stroke_count = UInt16(20)
    zone_count = UInt16(21)
    event = EventField(0)
    event_type = EventType(1)
    swim_stroke = SwimStroke(7)
    avg_swimming_cadence = UInt8(9)
    event_group = UInt8(10)
    length_type = LengthType(12)


class Record(Message):
    msg_type = 20

    timestamp = DateTime(253)
    position_lat = Degrees(0)
    position_long = Degrees(1)
    distance = Distance(5)
    time_from_course = UInt32(11)
    total_cycles = Cycles(19)
    accumulated_power = UInt32(29)
    altitude = Altitude(2)
    speed = Speed(6)
    power = Power(7)
    grade = Percents(9)
    compressed_accumulated_power = Power(28)
    vertical_speed = SSpeed(32)
    calories = Calories(33)
    vertical_oscillation = UInt16(39)
    stance_time_percent = StancePercents(40)
    stance_time = StanceTime(41)
    ball_speed = BallSpeed(51)
    cadence256 = UInt16(52)
    total_hemoglobin_conc = Hemoglobin(54)
    total_hemoglobin_conc_min = Hemoglobin(55)
    total_hemoglobin_conc_max = Hemoglobin(56)
    saturated_hemoglobin_percent = HemoglobinPercents(57)
    saturated_hemoglobin_percent_min = HemoglobinPercents(58)
    saturated_hemoglobin_percent_max = HemoglobinPercents(59)
    heart_rate = HeartRate(3)
    cadence = Cadence(4)
    compressed_speed_distance = Byte(8, count=3)
    resistance = UInt8(10)
    cycle_length = UInt8(12)
    temperature = Temperature(13)
    speed_1s = UInt8(17)
    cycles = UInt8(18)
    left_right_balance = LeftRightBalance(30)
    grps_accuracy = Accuracy(31)
    activity_type = ActivityType(42)
    left_torque_effectiveness = UInt8(43)
    right_torque_effectiveness = UInt8(44)
    left_pedal_smoothness = UInt8(45)
    right_pedal_smoothness = UInt8(46)
    combined_pedal_smoothness = UInt8(47)
    time128 = UInt8(48)
    stroke_type = StrokeType(49)
    zone = UInt8(50)
    device_index = DeviceIndex(62)


class Event(Message):
    msg_type = 21

    timestamp = DateTime(253)
    data = UInt32(3)
    data16 = UInt16(2)
    score = UInt16(7)
    opponent_score = UInt16(8)
    event = EventField(0)
    event_type = EventType(1)
    event_group = UInt8(4)
    front_gear_num = UInt8Z(9)
    front_gear = UInt8Z(10)
    rear_gear_num = UInt8Z(11)
    rear_gear = UInt8Z(12)


class DeviceInfo(Message):
    msg_type = 23

    timestamp = DateTime(253)
    serial_number = UInt32Z(3)
    cum_operating_time = UInt32(7)
    manufacturer = Manufacturer(2)
    product = Product(4)
    software_version = Version(5)
    battery_voltage = UInt16(10)
    ant_device_number = UInt16Z(21)
    device_index = DeviceIndex(0)
    device_type = UInt8(1)
    hardware_version = UInt8(6)
    battery_status = BatteryStatus(11)
    sensor_position = BodyLocation(18)
    descriptor = String(19)
    ant_transmission_type = UInt8Z(20)
    ant_network = AntNetwork(22)
    source_type = SourceType(25)


class Hrv(Message):
    msg_type = 78

    time = TimerTime(0)
