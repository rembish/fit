from fit.types import UInt32Z, UInt16, UInt32, UInt8, SInt32, SInt16, SInt8, \
    String, Byte, UInt8Z, UInt16Z, DateTime, Manufacturer, File, \
    LocalDateTime, Activity, Event, EventType, MessageIndex, \
    LeftRightBalance100, LeftRightBalance, Sport, SubSport, SessionTrigger, \
    SwimStroke, DisplayMeasure, Intensity, LapTrigger, LengthType, \
    ActivityType, StrokeType, DeviceIndex, BatteryStatus, BodyLocation, \
    AntNetwork, SourceType, Type, Semicircles, Altitude


class Meta(dict):
    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value


class FieldProxy(object):
    def __init__(self, number, key):
        self.number = number
        self.key = key

    def __get__(self, instance, owner):
        return instance._data.get(self.key, None)

    def __set__(self, instance, value):
        instance._data[self.key] = value

    def __delete__(self, instance):
        instance._data[self.key] = None


class MessageMeta(type):
    def __new__(cls, name, bases, attrs):
        meta = Meta()
        meta.model = {}
        meta.names = {}

        for key, value in attrs.items():
            if isinstance(value, Type):
                meta.model[value.number] = value
                meta.names[value.number] = key

        for key in meta.names.values():
            attrs.pop(key)

        attrs['_meta'] = meta
        instance = super(MessageMeta, cls).__new__(cls, name, bases, attrs)

        for number, key in meta.names.items():
            setattr(instance, key, FieldProxy(number, key))

        return instance


class Message(object):
    __metaclass__ = MessageMeta

    msg_type = -1

    def __init__(self, definition):
        self._data = {}
        self._definition = definition

    def __repr__(self):
        return '<%s[%d] %s>' % (
            self.__class__.__name__, self.msg_type,
            ' '.join("%s=%s" % (
                self._meta.names[field.number],
                self._meta.model[field.number].readable(getattr(
                    self, self._meta.names[field.number]))
            ) for field in self._definition.fields
            if getattr(self, self._meta.names[field.number]) is not None)
        )

    def read(self, buffer):
        unknown = 0
        for field in self._definition.fields:
            if field.number not in self._meta.names:
                self._meta.names[field.number] = "unknown_%d" % unknown
                self._meta.model[field.number] = field
                unknown += 1

            setattr(
                self, self._meta.names[field.number],
                field.read(
                    buffer, architecture=self._definition.architecture))

    def write(self, index):
        from fit.record.header import DataHeader

        buffer = DataHeader(index).write()
        for field in self._definition.fields:
            value = getattr(self, self._meta.names[field.number])
            buffer += field.write(value)
        return buffer


class GenericMessage(Message):
    def __init__(self, definition):
        super(GenericMessage, self).__init__(definition)
        self.msg_type = None


class FileIdMessage(Message):
    msg_type = 0

    serial_number = UInt32Z(3)
    time_created = DateTime(4)
    manufacturer = Manufacturer(1)
    product = UInt16(2)
    number = UInt16(5)
    type = File(0)


class FileCreatorMessage(Message):
    msg_type = 49

    software_version = UInt16(0)
    hardware_version = UInt8(1)


class ActivityMessage(Message):
    msg_type = 34

    timestamp = DateTime(253)
    total_timer_time = UInt32(0)
    local_timestamp = LocalDateTime(5)
    num_sessions = UInt16(1)
    type = Activity(2)
    event = Event(3)
    event_type = EventType(4)
    event_group = UInt8(6)


class SessionMessage(Message):
    msg_type = 18

    timestamp = DateTime(253)
    start_time = DateTime(2)
    start_position_lat = Semicircles(3)
    start_position_long = Semicircles(4)
    total_elapsed_time = UInt32(7)
    total_timer_time = UInt32(8)
    total_distance = UInt32(9)
    total_cycles = UInt32(10)
    nec_lat = Semicircles(29)
    nec_long = Semicircles(30)
    swc_lat = Semicircles(31)
    swc_long = Semicircles(32)
    avg_stroke_count = UInt32(41)
    total_work = UInt32(48)
    total_moving_time = UInt32(59)
    time_in_hr_zone = UInt32(65)
    time_in_speed_zone = UInt32(66)
    time_in_cadence_zone = UInt32(67)
    time_in_power_zone = UInt32(68)
    avg_lap_time = UInt32(69)
    message_index = MessageIndex(254)
    total_calories = UInt16(11)
    total_fat_calories = UInt16(13)
    avg_speed = UInt16(14)
    max_speed = UInt16(15)
    avg_power = UInt16(20)
    max_power = UInt16(21)
    total_ascent = UInt16(22)
    total_descent = UInt16(23)
    first_lap_index = UInt16(25)
    num_laps = UInt16(26)
    normalized_power = UInt16(34)
    training_stress_score = UInt16(35)
    intensity_factor = UInt16(36)
    left_right_balance = LeftRightBalance100(37)
    avg_stroke_distance = UInt16(42)
    pool_length = UInt16(44)
    num_active_lengths = UInt16(47)
    avg_altitude = Altitude(49)
    max_altitude = Altitude(50)
    avg_grade = SInt16(52)
    avg_pos_grade = SInt16(53)
    avg_neg_grade = SInt16(54)
    max_pos_grade = SInt16(55)
    max_neg_grade = SInt16(56)
    avg_pos_vertical_speed = SInt16(60)
    avg_neg_vertical_speed = SInt16(61)
    max_pos_vertical_speed = SInt16(62)
    max_neg_vertical_speed = SInt16(63)
    best_lap_index = UInt16(70)
    min_altitude = Altitude(71)
    player_score = UInt16(82)
    opponent_score = UInt16(83)
    stroke_count = UInt16(85)
    zone_count = UInt16(86)
    max_ball_speed = UInt16(87)
    avg_ball_speed = UInt16(88)
    avg_vertical_oscillation = UInt16(89)
    avg_stance_time_percent = UInt16(90)
    avg_stance_time = UInt16(91)
    event = Event(0)
    event_type = EventType(1)
    sport = Sport(5)
    sub_sport = SubSport(6)
    avg_heart_rate = UInt8(16)
    max_heart_rate = UInt8(17)
    avg_cadence = UInt8(18)
    max_cadence = UInt8(19)
    total_training_effect = UInt8(24)
    event_group = UInt8(27)
    trigger = SessionTrigger(28)
    swim_stroke = SwimStroke(43)
    pool_length_unit = DisplayMeasure(46)
    gps_accuracy = UInt8(51)
    avg_temperature = SInt8(57)
    max_temperature = SInt8(58)
    min_heart_rate = UInt8(64)
    opponent_name = String(84)
    avg_fractional_cadence = UInt8(92)
    max_fractional_cadence = UInt8(93)
    total_fractional_cycles = UInt8(94)


class LapMessage(Message):
    msg_type = 19

    timestamp = DateTime(253)
    start_time = DateTime(2)
    start_position_lat = Semicircles(3)
    start_position_long = Semicircles(4)
    end_position_lat = Semicircles(5)
    end_position_long = Semicircles(6)
    total_elapsed_time = UInt32(7)
    total_timer_time = UInt32(8)
    total_distance = UInt32(9)
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
    max_speed = UInt16(14)
    avg_power = UInt16(19)
    max_power = UInt16(20)
    total_ascent = UInt16(21)
    total_descent = UInt16(22)
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
    avg_total_hemoglobin_conc = UInt16(84)
    min_total_hemoglobin_conc = UInt16(85)
    max_total_hemoglobin_conc = UInt16(86)
    avg_saturated_hemoglobin_percent = UInt16(87)
    min_saturated_hemoglobin_percent = UInt16(88)
    max_saturated_hemoglobin_percent = UInt16(89)
    event = Event(0)
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


class LengthMessage(Message):
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
    event = Event(0)
    event_type = EventType(1)
    swim_stroke = SwimStroke(7)
    avg_swimming_cadence = UInt8(9)
    event_group = UInt8(10)
    length_type = LengthType(12)


class RecordMessage(Message):
    msg_type = 20

    timestamp = DateTime(253)
    position_lat = Semicircles(0)
    position_long = Semicircles(1)
    distance = UInt32(5)
    time_from_course = UInt32(11)
    total_cycles = UInt32(19)
    accumulated_power = UInt32(29)
    altitude = Altitude(2)
    speed = UInt16(6)
    power = UInt16(7)
    grade = SInt16(9)
    compressed_accumulated_power = UInt16(28)
    vertical_speed = SInt16(32)
    calories = UInt16(33)
    vertical_oscillation = UInt16(39)
    stance_time_percent = UInt16(40)
    stance_time = UInt16(41)
    ball_speed = UInt16(51)
    cadence256 = UInt16(52)
    total_hemoglobin_conc = UInt16(54)
    total_hemoglobin_conc_min = UInt16(55)
    total_hemoglobin_conc_max = UInt16(56)
    saturated_hemoglobin_percent = UInt16(57)
    saturated_hemoglobin_percent_min = UInt16(58)
    saturated_hemoglobin_percent_max = UInt16(59)
    heart_rate = UInt8(3)
    cadence = UInt8(4)
    compressed_speed_distance = Byte(8, count=3)
    resistance = UInt8(10)
    cycle_length = UInt8(12)
    temperature = SInt8(13)
    speed_1s = UInt8(17)
    cycles = UInt8(18)
    left_right_balance = LeftRightBalance(30)
    grps_accuracy = UInt8(31)
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


class EventMessage(Message):
    msg_type = 21

    timestamp = DateTime(253)
    data = UInt32(3)
    data16 = UInt16(2)
    score = UInt16(7)
    opponent_score = UInt16(8)
    event = Event(0)
    event_type = EventType(1)
    event_group = UInt8(4)
    front_gear_num = UInt8Z(9)
    front_gear = UInt8Z(10)
    rear_gear_num = UInt8Z(11)
    rear_gear = UInt8Z(12)


class DeviceInfoMessage(Message):
    msg_type = 23

    timestamp = DateTime(253)
    serial_number = UInt32Z(3)
    cum_operating_time = UInt32(7)
    manufacturer = Manufacturer(2)
    product = UInt16(4)
    software_version = UInt16(5)
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

    time = UInt16(0)


KNOWN = {
    0: FileIdMessage,
    49: FileCreatorMessage,
    34: ActivityMessage,
    18: SessionMessage,
    19: LapMessage,
    101: LengthMessage,
    20: RecordMessage,
    21: EventMessage,
    23: DeviceInfoMessage,
    78: Hrv,
}
