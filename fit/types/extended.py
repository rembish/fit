# coding=utf-8
from datetime import datetime
from time import mktime

from fit.types.general import UInt32, UInt16, UInt8, Enum, UInt32Z, UInt8Z
from fit.types.mixins import KnownMixin, ScaleMixin


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
        0x8000: "Selected",
        0x7000: "Reserved",
        0x0fff: "Mask"
    }


class LeftRightBalance(KnownMixin, UInt8):
    known = {
        0x7f: "Mask",
        0x80: "Right"
    }


class LeftRightBalance100(KnownMixin, UInt16):
    known = {
        0x3fff: "Mask",
        0x8000: "Right"
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
        0: "File ID",
        1: "Capabilities",
        2: "Device Settings",
        3: "User Profile",
        4: "HRM Profile",
        5: "SDM Profile",
        6: "Bike Profile",
        7: "Zones Target",
        8: "HR Zone",
        9: "Power Zone",
        10: "Met Zone",
        12: "Sport",
        15: "Goal",
        18: "Session",
        19: "Lap",
        20: "Record",
        21: "Event",
        23: "Device Info",
        26: "Workout",
        27: "Workout Step",
        28: "Schedule",
        30: "Weight Scale",
        31: "Course",
        32: "Course Point",
        33: "Totals",
        34: "Activity",
        35: "Software",
        37: "File Capabilities",
        38: "Mesg Capabilities",
        39: "Field Capabilities",
        49: "File Creator",
        51: "Blood Pressure",
        53: "Speed Zone",
        55: "Monitoring",
        78: "HRV",
        101: "Length",
        103: "Monitoring Info",
        105: "Pad",
        106: "Slave Device",
        132: "Cadence Zone",
        145: "Memo Glob",
        0xff00: "Mfg Range Min",  # 0xFF00 - 0xFFFE reserved for manufacturer
        0xfffe: "Mfg Range Max",  # specific messages
    }


class Weight(ScaleMixin, KnownMixin, UInt16):
    known = {
        0xfffe: "Calculating"
    }
    units = "kg"

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
        0x0000: "Local Min",
        0x000F: "Local Max",
        0x0010: "Stationary Min",
        0x00FF: "Stationary Max",
        0x0100: "Portable Min",
        0xFFFE: "Portable Max",
    }

class AntplusDeviceType(KnownMixin, UInt8):
    known = {  # to be done
        1: "antfs",
        11: "bike_power",
    }


class CourseCapabilities(KnownMixin, UInt32Z):
    known = {
        0x00000001: "Processed",
        0x00000002: "Valid",
        0x00000004: "Time",
        0x00000008: "Distance",
        0x00000010: "Position",
        0x00000020: "Heart Rate",
        0x00000040: "Power",
        0x00000080: "Cadence",
        0x00000100: "Training",
        0x00000200: "Navigation",
    }


class WorkoutCapabilities(KnownMixin, UInt32Z):
    known = {
        0x00000001: "Interval",
        0x00000002: "Custom",
        0x00000004: "Fitness Equipment",
        0x00000008: "Firstbeat",
        0x00000010: "New Leaf",
        0x00000020: "TCX",  # for backwards compatibility. Watch should add
                            # missing id fields then clear flag
        0x00000080: "Speed",  # Speed source required for workout step
        0x00000100: "Heart Rate",  # Heart rate src required for workout step
        0x00000200: "Distance",  # Distance source required for workout step
        0x00000400: "Cadence",  # Cadence source required for workout step
        0x00000800: "Power",  # Power source required for workout step
        0x00001000: "Grade",  # Grade source required for workout step
        0x00002000: "Resistance",  # Resistance src required for workout step
        0x00004000: "Protected",
    }


class ConnectivityCapabilities(KnownMixin, UInt32Z):
    known = {
        0x00000001: "Bluetooth",
        0x00000002: "Bluetooth LE",
        0x00000004: "ANT",
        0x00000008: "Activity Upload",
        0x00000010: "Course Download",
        0x00000020: "Workout Download",
        0x00000040: "Live Track",
        0x00000080: "Weather Conditions",
        0x00000100: "Weather Alerts",
        0x00000200: "GPS Ephemeris Download",
        0x00000400: "Explicit Archive",
        0x00000800: "Setup Incomplete",
    }


class SportBits0(KnownMixin, UInt8Z):
    known = {
        0x01: "Generic",
        0x02: "Running",
        0x04: "Cycling",
        0x08: "Transition",  # Multisport transition
        0x10: "Fitness Equipment",
        0x20: "Swimming",
        0x40: "Basketball",
        0x80: "Soccer",
    }


class FileFlags(KnownMixin, UInt8Z):
    known = {
        0x02: "Read",
        0x04: "Write",
        0x08: "Erase",
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
        0: "Activity End",
        1: "Manual",
        2: "Auto Multi Sport",
        3: "Fitness Equipment",
    }


class SwimStroke(Enum):
    variants = {
        0: "Freestyle",
        1: "Backstroke",
        2: "Breaststroke",
        3: "Butterfly",
        4: "Drill",
        5: "Mixed",
        6: "IM"
    }


class DisplayMeasure(Enum):
    variants = {
        0: "Metric",
        1: "Statute",
    }


class Intensity(Enum):
    variants = {
        0: "Active",
        1: "Rest",
        2: "Warm Up",
        3: "Cool Down",
    }


class LapTrigger(Enum):
    variants = {
        0: "Manual",
        1: "Time",
        2: "Distance",
        3: "Position Start",
        4: "Position Lap",
        5: "Position Waypoint",
        6: "Position Marked",
        7: "Session End",
        8: "Fitness Equipment",
    }


class LengthType(Enum):
    variants = {
        0: "Idle",
        1: "Active",
    }


class ActivityType(Enum):
    variants = {
        0: "Generic",
        1: "Running",
        2: "Cycling",
        3: "Transition",
        4: "Fitness Equipment",
        5: "Swimming",
        6: "Walking",
        254: "All",
    }


class StrokeType(Enum):
    variants = {
        0: "No Event",
        1: "Other",
        2: "Serve",
        3: "Forehand",
        4: "Backhand",
        5: "Smash",
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
        0: "Normal",
        1: "Irregular",
    }


class BpStatus(Enum):
    variants = {
        0: "No Error",
        1: "Error Incomplete Data",
        2: "Error Non Measurement",
        3: "Error Data out of Range",
        4: "Error Irregular Heart Rate",
    }


class CoursePoint(Enum):
    variants = {
        0: "Generic",
        1: "Summit",
        2: "Valley",
        3: "Water",
        4: "Food",
        5: "Danger",
        6: "Left",
        7: "Right",
        8: "Straight",
        9: "First Aid",
        10: "Fourth Category",
        11: "Third Category",
        12: "Second Category",
        13: "First Category",
        14: "Hors Catégorie",
        15: "Spring",
        16: "Left Fork",
        17: "Right Fork",
        18: "Middle Fork",
        19: "Slight Left",
        20: "Sharp Left",
        21: "Slight Right",
        22: "Sharp Right",
        23: "U Turn"
    }


class MesgCount(Enum):
    variants = {
        0: "Num per File",
        1: "Max per File",
        2: "Max per File Type",
    }


class Goal(Enum):
    variants = {
        0: "Time",
        1: "Distance",
        2: "Calories",
        3: "Frequency",
        4: "Steps",
    }


class GoalRecurrence(Enum):
    variants = {
        0: "Off",
        1: "Daily",
        2: "Weekly",
        3: "Monthly",
        4: "Yearly",
        5: "Custom",
    }


class Schedule(Enum):
    variants = {
        0: "Workout",
        1: "Course",
    }


class HrZoneCalc(Enum):
    variants = {
        0: "Custom",
        1: "Percent Max HR",
        2: "Percent HRR",
    }


class PwrZoneCalc(Enum):
    variants = {
        0: "Custom",
        1: "Percent FTP",
    }


class WktStepDuration(Enum):
    variants = {
        0: "Time",
        1: "Distance",
        2: "HR less than",
        3: "HR greater than",
        4: "Calories",
        5: "Open",
        6: "Repeat until Steps Complete",
        7: "Repeat until Time",
        8: "Repeat until Distance",
        9: "Repeat until Calories",
        10: "Repeat until HR less than",
        11: "Repeat until HR greater than",
        12: "Repeat until Power less than",
        13: "Repeat until Power greater than",
        14: "Power less than",
        15: "Power greater than",
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
        0: "Generic",
        1: "Treadmill",  # Run...
        2: "Street",
        3: "Trail",
        4: "Track",
        5: "Spin",  # Cycling...
        6: "Indoor Cycling",
        7: "Road",
        8: "Mountain",
        9: "Downhill",
        10: "Recumbent",
        11: "Cyclocross",
        12: "Hand Cycling",
        13: "Track Cycling",
        14: "Indoor Rowing",  # Fitness Equipment..
        15: "Elliptical",
        16: "Stair Climbing",
        17: "Swimming",  # Swimming...
        18: "Open Water",
        254: "All",
    }


class ActivityLevel(Enum):
    variants = {
        0: "Low",
        1: "Medium",
        2: "High",
    }


class Gender(Enum):
    variants = {
        0: "Female",
        1: "Male",
    }


class Language(Enum):
    variants = {
        0: "English",
        1: "French",
        2: "Italian",
        3: "German",
        4: "Spanish",
        5: "Croatian",
        6: "Czech",
        7: "Danish",
        8: "Dutch",
        9: "Finnish",
        10: "Greek",
        11: "Hungarian",
        12: "Norwegian",
        13: "Polish",
        14: "Portuguese",
        15: "Slovakian",
        16: "Slovenian",
        17: "Swedish",
        18: "Russian",
        19: "Turkish",
        20: "Latvian",
        21: "Ukrainian",
        22: "Arabic",
        23: "Farsi",
        24: "Bulgarian",
        25: "Romanian",
        254: "Custom",
    }


class DisplayHeart(Enum):
    variants = {
        0: "BPM",
        1: "Max",
        2: "Reserve",
    }


class DisplayPower(Enum):
    variants = {
        0: "Watts",
        1: "Percent FTP",
    }


class DisplayPosition(Enum):
    variants = {  # to be done
        0: "Degree",  # dd.dddddd
    }


class ActivityClass(Enum):
    variants = {
        100: "Level Max",
        0x80: "Athlete"
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
