from datetime import datetime
from time import mktime

from fit.types.general import UInt32, UInt16, UInt8, Enum, UInt32Z, UInt8Z
from fit.types.helpers import KnownMixin


class LocalDateTime(UInt32):
    start_ts = 631062000  # 00:00 Dec 31 1989

    def _load(self, data):
        return datetime.fromtimestamp(self.start_ts + data)

    def _save(self, value):
        return int(mktime(value.timetuple()) - self.start_ts)


class DateTime(LocalDateTime):
    pass


class Manufacturer(KnownMixin, UInt16):
    known = {  # to be done
        1: "garmin",
        13: "dynastream_oem",
        15: "dynastream",
        255: "development",
    }


class GarminProduct(KnownMixin, UInt16):
    known = {  # to be done
        1: "hrm1",
        1124: "fr110",
        1551: "fenix",
        65534: "connect",
    }


class MessageIndex(KnownMixin, UInt16):
    known = {
        0x8000: "selected",
        0x7000: "reserved",
        0x0fff: "mask"
    }


class LeftRightBalance(KnownMixin, UInt8):
    known = {
        0x7f: "mask",
        0x80: "right"
    }


class LeftRightBalance100(KnownMixin, UInt16):
    known = {
        0x3fff: "mask",
        0x8000: "right"
    }


class DeviceIndex(KnownMixin, UInt8):
    known = {
        0: "creator",
    }


class BatteryStatus(KnownMixin, UInt8):
    known = {
        1: "new",
        2: "good",
        3: "ok",
        4: "low",
        5: "critical",
    }


class MesgNum(KnownMixin, UInt16):
    known = {
        0: "file_id",
        1: "capabilities",
        2: "device_settings",
        3: "user_profile",
        4: "hrm_profile",
        5: "sdm_profile",
        6: "bike_profile",
        7: "zones_target",
        8: "hr_zone",
        9: "power_zone",
        10: "met_zone",
        12: "sport",
        15: "goal",
        18: "session",
        19: "lap",
        20: "record",
        21: "event",
        23: "device_info",
        26: "workout",
        27: "workout_step",
        28: "schedule",
        30: "weight_scale",
        31: "course",
        32: "course_point",
        33: "totals",
        34: "activity",
        35: "software",
        37: "file_capabilities",
        38: "mesg_capabilities",
        39: "field_capabilities",
        49: "file_creator",
        51: "blood_pressure",
        53: "speed_zone",
        55: "monitoring",
        78: "hrv",
        101: "length",
        103: "monitoring_info",
        105: "pad",
        106: "slave_device",
        132: "cadence_zone",
        145: "memo_glob",
        0xff00: "mfg_range_min",  # 0xFF00 - 0xFFFE reserved for manufacturer
        0xfffe: "mfg_range_max",  # specific messages
    }


class Weight(KnownMixin, UInt16):
    known = {
        0xfffe: "calculating"
    }

    def _load(self, data):
        value = KnownMixin._load(self, data)
        if value == data:
            return super(Weight, self)._load(data)
        return value

    def _save(self, value):
        data = KnownMixin._save(self, value)
        if data == value:
            return super(Weight, self)._save(value)
        return data


class UserLocalId(KnownMixin, UInt16):
    known = {
        0x0000: "local_min",
        0x000F: "local_max",
        0x0010: "stationary_min",
        0x00FF: "stationary_max",
        0x0100: "portable_min",
        0xFFFE: "portable_max",
    }


class AntplusDeviceType(KnownMixin, UInt8):
    known = {  # to be done
        1: "antfs",
        11: "bike_power",
    }


class CourseCapabilities(KnownMixin, UInt32Z):
    known = {
        0x00000001: "processed",
        0x00000002: "valid",
        0x00000004: "time",
        0x00000008: "distance",
        0x00000010: "position",
        0x00000020: "heart_rate",
        0x00000040: "power",
        0x00000080: "cadence",
        0x00000100: "training",
        0x00000200: "navigation",
    }


class WorkoutCapabilities(KnownMixin, UInt32Z):
    known = {
        0x00000001: "interval",
        0x00000002: "custom",
        0x00000004: "fitness_equipment",
        0x00000008: "firstbeat",
        0x00000010: "new_leaf",
        0x00000020: "tcx",  # for backwards compatibility. Watch should add
                            # missing id fields then clear flag
        0x00000080: "speed",  # Speed source required for workout step
        0x00000100: "heart_rate",  # Heart rate src required for workout step
        0x00000200: "distance",  # Distance source required for workout step
        0x00000400: "cadence",  # Cadence source required for workout step
        0x00000800: "power",  # Power source required for workout step
        0x00001000: "grade",  # Grade source required for workout step
        0x00002000: "resistance",  # Resistance src required for workout step
        0x00004000: "protected",
    }


class ConnectivityCapabilities(KnownMixin, UInt32Z):
    known = {
        0x00000001: "bluetooth",
        0x00000002: "bluetooth_le",
        0x00000004: "ant",
        0x00000008: "activity_upload",
        0x00000010: "course_download",
        0x00000020: "workout_download",
        0x00000040: "live_track",
        0x00000080: "weather_conditions",
        0x00000100: "weather_alerts",
        0x00000200: "gps_ephemeris_download",
        0x00000400: "explicit_archive",
        0x00000800: "setup_incomplete",
    }


class SportBits0(KnownMixin, UInt8Z):
    known = {
        0x01: "generic",
        0x02: "running",
        0x04: "cycling",
        0x08: "transition",  # Multisport transition
        0x10: "fitness_equipment",
        0x20: "swimming",
        0x40: "basketball",
        0x80: "soccer",
    }


class FileFlags(KnownMixin, UInt8Z):
    known = {
        0x02: "read",
        0x04: "write",
        0x08: "erase",
    }


class File(Enum):
    variants = {
        1: "device",
        2: "settings",
        3: "sport",
        4: "activity",
        5: "workout",
        6: "course",
        7: "schedules",
        9: "weight",
        10: "totals",
        11: "goals",
        14: "blood_pressure",
        15: "monitoring_a",
        20: "activity_summary",
        28: "monitoring_daily",
        32: "monitoring_b",
    }


class Activity(Enum):
    variants = {
        0: "manual",
        1: "auto_multi_sport",
    }


class Bool(Enum):
    variants = {
        0: False,
        1: True,
    }


class Event(Enum):
    variants = {
        0: "timer",
        3: "workout",
        4: "workout_step",
        5: "power_down",
        6: "power_up",
        7: "off_course",
        8: "session",
        9: "lap",
        10: "course_point",
        11: "battery",
        12: "virtual_partner_pace",
        13: "hr_high_alert",
        14: "hr_low_alert",
        15: "speed_high_alert",
        16: "speed_low_alert",
        17: "cad_high_alert",
        18: "cad_low_alert",
        19: "power_high_alert",
        20: "power_low_alert",
        21: "recovery_hr",
        22: "battery_low",
        23: "time_duration_alert",
        24: "distance_duration_alert",
        25: "calorie_duration_alert",
        26: "activity",
        27: "fitness_equipment",
        28: "length",
        32: "user_marker",
        33: "sport_point",
        36: "calibration",
        42: "front_gear_change",
        43: "rear_gear_change",
    }


class EventType(Enum):
    variants = {
        0: "start",
        1: "stop",
        2: "consecutive_depreciated",
        3: "marker",
        4: "stop_all",
        5: "begin_depreciated",
        6: "end_depreciated",
        7: "end_all_depreciated",
        8: "stop_disable",
        9: "stop_disable_all"
    }


class Sport(Enum):
    variants = {
        0: "generic",
        1: "running",
        2: "cycling",
        3: "transition",
        4: "fitness_equipment",
        5: "swimming",
        6: "basketball",
        7: "soccer",
        8: "tennis",
        9: "american_football",
        10: "training",
        11: "walking",
        12: "cross_country_skiing",
        13: "alpine_skiing",
        14: "snowboarding",
        15: "rowing",
        16: "mountaineering",
        17: "hiking",
        18: "multisport",
        19: "padding",
        254: "all",
    }


class SubSport(Enum):
    variants = {
        0: "generic",
        1: "treadmill",
        2: "street",
        3: "trail",
        4: "track",
        5: "spin",
        6: "indoor_cycling",
        7: "road",
        8: "mountain",
        9: "downhill",
        10: "recumbent",
        11: "cyclocross",
        12: "hand_cycling",
        13: "track_cycling",
        14: "indoor_rowing",
        15: "elliptical",
        16: "stair_climbing",
        17: "lap_swimming",
        18: "open_water",
        19: "flexibility_training",
        20: "strength_training",
        21: "warm_up",
        22: "match",
        23: "exercise",
        24: "challenge",
        25: "indoor_skiing",
        26: "cardio_training",
        254: "all",
    }


class SessionTrigger(Enum):
    variants = {
        0: "activity_end",
        1: "manual",
        2: "auto_multi_sport",
        3: "fitness_equipment",
    }


class SwimStroke(Enum):
    variants = {
        0: "freestyle",
        1: "backstroke",
        2: "breaststroke",
        3: "butterfly",
        4: "drill",
        5: "mixed",
        6: "im"
    }


class DisplayMeasure(Enum):
    variants = {
        0: "metric",
        1: "statute",
    }


class Intensity(Enum):
    variants = {
        0: "active",
        1: "rest",
        2: "warm_up",
        3: "cool_down",
    }


class LapTrigger(Enum):
    variants = {
        0: "manual",
        1: "time",
        2: "distance",
        3: "position_start",
        4: "position_lap",
        5: "position_waypoint",
        6: "position_marked",
        7: "session_end",
        8: "fitness_equipment",
    }


class LengthType(Enum):
    variants = {
        0: "idle",
        1: "active",
    }


class ActivityType(Enum):
    variants = {
        0: "generic",
        1: "running",
        2: "cycling",
        3: "transition",
        4: "fitness_equipment",
        5: "swimming",
        6: "walking",
        254: "all",
    }


class StrokeType(Enum):
    variants = {
        0: "no_event",
        1: "other",
        2: "serve",
        3: "forehand",
        4: "backhand",
        5: "smash",
    }


class BodyLocation(Enum):
    variants = {
        0: "left_leg",
        1: "left_calf",
        2: "left_shin",
        3: "left_hamstring",
        4: "left_quad",
        5: "left_glute",
        6: "right_leg",
        7: "right_calf",
        8: "right_shin",
        9: "right_hamstring",
        10: "right_quad",
        11: "right_glute",
        12: "torso_back",
        13: "left_lower_back",
        14: "left_upper_back",
        15: "right_lower_back",
        16: "right_upper_back",
        17: "torso_front",
        18: "left_abdomen",
        19: "left_chest",
        20: "right_abdomen",
        21: "right_chest",
        22: "left_arm",
        23: "left_shoulder",
        24: "left_bicep",
        25: "left_tricep",
        26: "left_brachioradialis",
        27: "left_forearm_extensors",
        28: "right_arm",
        29: "right_shoulder",
        30: "right_bicep",
        31: "right_tricep",
        32: "right_brachioradialis",
        33: "right_forearm_extensors",
        34: "neck",
        35: "throat",

    }


class AntNetwork(Enum):
    variants = {
        0: "public",
        1: "antplus",
        2: "antfs",
        3: "private",
    }


class SourceType(Enum):
    variants = {
        0: "ant",
        1: "antplus",
        2: "bluetooth",
        3: "bluetooth_low_energy",
        4: "wifi",
        5: "local",
    }


class HrType(Enum):
    variants = {
        0: "normal",
        1: "irregular",
    }


class BpStatus(Enum):
    variants = {
        0: "no_error",
        1: "error_incomplete_data",
        2: "error_non_measurement",
        3: "error_data_out_of_range",
        4: "error_irregular_heart_rate",
    }


class CoursePoint(Enum):
    variants = {
        0: "generic",
        1: "summit",
        2: "valley",
        3: "water",
        4: "food",
        5: "danger",
        6: "left",
        7: "right",
        8: "straight",
        9: "first_aid",
        10: "fourth_category",
        11: "third_category",
        12: "second_category",
        13: "first_category",
        14: "hors_categorie",
        15: "spring",
        16: "left_fork",
        17: "right_fork",
        18: "middle_fork",
        19: "slight_left",
        20: "sharp_left",
        21: "slight_right",
        22: "sharp_right",
        23: "u_turn"
    }


class MesgCount(Enum):
    variants = {
        0: "num_per_file",
        1: "max_per_file",
        2: "max_per_file_type",
    }


class Goal(Enum):
    variants = {
        0: "time",
        1: "distance",
        2: "calories",
        3: "frequency",
        4: "steps",
    }


class GoalRecurrence(Enum):
    variants = {
        0: "off",
        1: "daily",
        2: "weekly",
        3: "monthly",
        4: "yearly",
        5: "custom",
    }


class Schedule(Enum):
    variants = {
        0: "workout",
        1: "course",
    }


class HrZoneCalc(Enum):
    variants = {
        0: "custom",
        1: "percent_max_hr",
        2: "percent_hrr",
    }


class PwrZoneCalc(Enum):
    variants = {
        0: "custom",
        1: "percent_ftp",
    }


class WktStepDuration(Enum):
    variants = {
        0: "time",
        1: "distance",
        2: "hr_less_than",
        3: "hr_greater_than",
        4: "calories",
        5: "open",
        6: "repeat_until_steps_complete",
        7: "repeat_until_time",
        8: "repeat_until_distance",
        9: "repeat_until_calories",
        10: "repeat_until_hr_less_than",
        11: "repeat_until_hr_greater_than",
        12: "repeat_until_power_less_than",
        13: "repeat_until_power_greater_than",
        14: "rower_less_than",
        15: "rower_greater_than",
    }


class WktStepTarget(Enum):
    variants = {
        0: "Speed",
        1: "Heart Rate",
        2: "Open",
        3: "Cadence",
        4: "Power",
        5: "Grade",
        6: "Resistance",
    }


class ActivitySubType(Enum):
    variants = {
        0: "generic",
        1: "treadmill",  # Run...
        2: "street",
        3: "trail",
        4: "track",
        5: "spin",  # Cycling...
        6: "indoor_cycling",
        7: "road",
        8: "mountain",
        9: "downhill",
        10: "recumbent",
        11: "cyclocross",
        12: "hand_cycling",
        13: "track_cycling",
        14: "indoor_rowing",  # Fitness Equipment..
        15: "elliptical",
        16: "stair_climbing",
        17: "swimming",  # Swimming...
        18: "open_water",
        254: "all",
    }


class ActivityLevel(Enum):
    variants = {
        0: "low",
        1: "medium",
        2: "high",
    }


class Gender(Enum):
    variants = {
        0: "female",
        1: "male",
    }


class Language(Enum):
    variants = {
        0: "english",
        1: "french",
        2: "italian",
        3: "german",
        4: "spanish",
        5: "croatian",
        6: "czech",
        7: "danish",
        8: "dutch",
        9: "finnish",
        10: "greek",
        11: "hungarian",
        12: "norwegian",
        13: "polish",
        14: "portuguese",
        15: "slovakian",
        16: "slovenian",
        17: "swedish",
        18: "russian",
        19: "turkish",
        20: "latvian",
        21: "ukrainian",
        22: "arabic",
        23: "farsi",
        24: "bulgarian",
        25: "romanian",
        254: "custom",
    }


class DisplayHeart(Enum):
    variants = {
        0: "bpm",
        1: "max",
        2: "reserve",
    }


class DisplayPower(Enum):
    variants = {
        0: "watts",
        1: "percent_ftp",
    }


class DisplayPosition(Enum):
    variants = {  # to be done
        0: "degree",  # dd.dddddd
    }


class ActivityClass(Enum):
    variants = {
        100: "level_max",
        0x80: "athlete"
    }

    def _load(self, data):
        if 0 < data < 0x7F:
            return data
        return super(ActivityClass, self)._load(data)

    def _save(self, value):
        if isinstance(value, int):
            return value
        return super(ActivityClass, self)._save(value)


class TimerTrigger(Enum):
    variants = {
        0: "manual",
        1: "auto",
        2: "fitness_equipment",
    }


class FitnessEquipmentState(Enum):
    variants = {
        0: "ready",
        1: "in_use",
        2: "paused",
        3: "unknown",  # lost connection to fitness equipment
    }
