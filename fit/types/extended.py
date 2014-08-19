# coding=utf-8
from datetime import datetime
from time import mktime

from fit.types.general import UInt32, UInt16, UInt8, Enum
from fit.types.mixins import KnownMixin


class LocalDateTime(UInt32):
    start_ts = 631062000  # 00:00 Dec 31 1989

    def _load(self, data):
        return datetime.fromtimestamp(self.start_ts + data)

    def _save(self, value):
        return int(mktime(value.timetuple()) - self.start_ts)


class DateTime(LocalDateTime):
    pass


class Manufacturer(KnownMixin, UInt16):
    known = {
        1: "Garmin",
        255: "Development"
        # to be done
    }


class Product(KnownMixin, UInt16):
    known = {
        1551: "Garmin Fēnix",
        65534: "Garmin Connect"
        # to be done
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
        0: "Creator",
    }


class BatteryStatus(KnownMixin, UInt8):
    known = {
        1: "New",
        2: "Good",
        3: "Ok",
        4: "Low",
        5: "Critical",
    }


class File(Enum):
    variants = {
        1: "Device",
        2: "Settings",
        3: "Sport",
        4: "Activity",
        5: "Workout",
        6: "Course",
        7: "Schedules",
        9: "Weight",
        10: "Totals",
        11: "Goals",
        14: "Blood Pressure",
        15: "Monitoring A",
        20: "Activity Summary",
        28: "Monitoring Daily",
        32: "Monitoring B",
    }


class Activity(Enum):
    variants = {
        0: "Manual",
        1: "Auto Multi Sport",
    }


class Event(Enum):
    variants = {
        0: "Timer",
        3: "Workout",
        4: "Workout Step",
        5: "Power Down",
        6: "Power Up",
        7: "Off Course",
        8: "Session",
        9: "Lap",
        10: "Course Point",
        11: "Battery",
        12: "Virtual Partner Pace",
        13: "HR High Alert",
        14: "HR Low Alert",
        15: "Speed High Alert",
        16: "Speed Low Alert",
        17: "Cad High Alert",
        18: "Cad Low Alert",
        19: "Power High Alert",
        20: "Power Low Alert",
        21: "Recovery HR",
        22: "Battery Low",
        23: "Time Duration Alert",
        24: "Distance Duration Alert",
        25: "Calorie Duration Alert",
        26: "Activity",
        27: "Fitness Equipment",
        28: "Length",
        32: "User Marker",
        33: "Sport Point",
        36: "Calibration",
        42: "Front Gear Change",
        43: "Rear Gear Change",
    }


class EventType(Enum):
    variants = {
        0: "Start",
        1: "Stop",
        2: "Consecutive Depreciated",
        3: "Marker",
        4: "Stop All",
        5: "Begin Depreciated",
        6: "End Depreciated",
        7: "End All Depreciated",
        8: "Stop Disable",
        9: "Stop Disable All"
    }


class Sport(Enum):
    variants = {
        0: "Generic",
        1: "Running",
        2: "Cycling",
        3: "Transition",
        4: "Fitness Equipment",
        5: "Swimming",
        6: "Basketball",
        7: "Soccer",
        8: "Tennis",
        9: "American Football",
        10: "Training",
        11: "Walking",
        12: "Cross Country Skiing",
        13: "Alpine Skiing",
        14: "Snowboarding",
        15: "Rowing",
        16: "Mountaineering",
        17: "Hiking",
        18: "Multisport",
        19: "Padding",
        254: "All",
    }


class SubSport(Enum):
    variants = {
        0: "Generic",
        1: "Treadmill",
        2: "Street",
        3: "Trail",
        4: "Track",
        5: "Spin",
        6: "Indoor Cycling",
        7: "Road",
        8: "Mountain",
        9: "Downhill",
        10: "Recumbent",
        11: "Cyclocross",
        12: "Hand Cycling",
        13: "Track Cycling",
        14: "Indoor Rowing",
        15: "Elliptical",
        16: "Stair Climbing",
        17: "Lap Swimming",
        18: "Open Water",
        19: "Flexibility Training",
        20: "Strength Training",
        21: "Warm Up",
        22: "Match",
        23: "Exercise",
        24: "Challenge",
        25: "Indoor Skiing",
        26: "Cardio Training",
        254: "All",
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
        0: "Left Leg",
        1: "Left Calf",
        2: "Left Shin",
        3: "Left Hamstring",
        4: "Left Quad",
        5: "Left Glute",
        6: "Right Leg",
        7: "Right Calf",
        8: "Right Shin",
        9: "Right Hamstring",
        10: "Right Quad",
        11: "Right Glute",
        12: "Torso Back",
        13: "Left Lower Back",
        14: "Left Upper Back",
        15: "Right Lower Back",
        16: "Right Upper Back",
        17: "Torso Front",
        18: "Left Abdomen",
        19: "Left Chest",
        20: "Right Abdomen",
        21: "Right Chest",
        22: "Left Arm",
        23: "Left Shoulder",
        24: "Left Bicep",
        25: "Left Tricep",
        26: "Left Brachioradialis",
        27: "Left Forearm Extensors",
        28: "Right Arm",
        29: "Right Shoulder",
        30: "Right Bicep",
        31: "Right Tricep",
        32: "Right Brachioradialis",
        33: "Right Forearm Extensors",
        34: "Neck",
        35: "Throat",

    }


class AntNetwork(Enum):
    variants = {
        0: "Public",
        1: "Ant+",
        2: "AntFS",
        3: "Private",
    }


class SourceType(Enum):
    variants = {
        0: "Ant",
        1: "Ant+",
        2: "Bluetooth",
        3: "Bluetooth Low Energy",
        4: "WiFi",
        5: "Local",
    }
