# coding=utf-8
from fit.types.general import SInt32, UInt16, UInt32, UInt8, SInt16, SInt8
from fit.types.mixins import ScaleMixin


class Degrees(ScaleMixin, SInt32):
    scale = 2 ** 31 / 180.
    units = "°"


class Altitude(ScaleMixin, UInt16):
    scale = 5
    offset = 500
    units = "m"


class TimerTime(ScaleMixin, UInt32):
    scale = 1000
    units = "s"


class Distance(ScaleMixin, UInt32):
    scale = 100
    units = "m"


class Difference(UInt16):
    units = "m"


class Cycles(UInt32):
    units = " cycles"


class Calories(UInt16):
    units = " KCal"


class Speed(ScaleMixin, UInt16):
    scale = 1000
    units = " m/s"


class SSpeed(ScaleMixin, SInt16):
    scale = 1000
    units = " m/s"


class BallSpeed(ScaleMixin, UInt16):
    units = " m/s"


class HeartRate(UInt8):
    units = " bpm"


class Cadence(UInt8):
    units = " rpm"


class Power(UInt16):
    units = " watts"


class StressScore(ScaleMixin, UInt16):
    scale = 10
    units = " tss"


class IntensityFactor(ScaleMixin, UInt16):
    scale = 1000
    units = " if"


class StrokeCount(ScaleMixin, UInt32):
    scale = 10
    units = " strokes/lap"


class Work(UInt32):
    units = "J"


class Percents(ScaleMixin, SInt16):
    scale = 100
    units = "%"


class UPercents(ScaleMixin, UInt16):
    scale = 100
    units = "%"


class Temperature(SInt8):
    units = "°C"


class Oscillation(ScaleMixin, UInt16):
    scale = 10
    units = "mm"


class StancePercents(ScaleMixin, UInt16):
    scale = 100
    units = "%"


class StanceTime(ScaleMixin, UInt16):
    scale = 10
    units = "ms"


class FractionalCadence(ScaleMixin, Cadence):
    scale = 128


class FractionalCycles(ScaleMixin, UInt8):
    scale = 128
    units = " cycles"


class Hemoglobin(ScaleMixin, UInt16):
    scale = 100
    units = " g/dL"


class HemoglobinPercents(ScaleMixin, UInt16):
    scale = 10
    units = "%"


class Accuracy(UInt8):
    units = "m"


class Pressure(UInt16):
    units = "mmHg"


class Version(UInt16):
    def _load(self, data):
        return str(data / 100.)

    def _save(self, value):
        return int(value * 100)


class Mass(ScaleMixin, UInt16):
    scale = 100
    units = "kg"


class Met(ScaleMixin, UInt16):
    scale = 4
    units = " KCal/day"


class Years(UInt8):
    units = "years"


class MetCalories(ScaleMixin, UInt16):
    scale = 10
    units = "KCal/min"


class MetFatCalories(ScaleMixin, UInt8):
    scale = 10
    units = "KCal/min"
