# coding=utf-8
from fit.types.general import SInt32, UInt16, UInt32, UInt8, SInt16, SInt8


class Degrees(SInt32):
    units = "°"

    def _load(self, data):
        return data * (180. / 2 ** 31)

    def _save(self, value):
        return int(value * (2 ** 31 / 180.))


class Altitude(UInt16):
    def _load(self, data):
        return (data / 5.) - 500.

    def _save(self, value):
        return int((value + 500.) * 5.)


class TimerTime(UInt32):
    units = "s"

    def _load(self, data):
        return data / 1000.

    def _save(self, value):
        return int(value * 1000.)


class Distance(UInt32):
    units = "m"

    def _load(self, data):
        return data / 100.

    def _save(self, value):
        return int(value * 100.)


class Difference(UInt16):
    units = "m"


class Cycles(UInt32):
    units = " cycles"


class Calories(UInt16):
    units = " KCal"


class Speed(UInt16):
    units = " m/s"

    def _load(self, data):
        return data / 1000.

    def _save(self, value):
        return int(value * 1000.)


class SSpeed(SInt16):
    units = " m/s"

    def _load(self, data):
        return data / 1000.

    def _save(self, value):
        return int(value * 1000.)


class BallSpeed(UInt16):
    units = " m/s"

    def _load(self, data):
        return data / 100.

    def _save(self, value):
        return int(value * 100.)


class HeartRate(UInt8):
    units = " bpm"


class Cadence(UInt8):
    units = " rpm"


class Power(UInt16):
    units = " watts"


class StressScore(UInt16):
    units = " tss"

    def _load(self, data):
        return data / 10.

    def _save(self, value):
        return int(value * 10.)


class IntensityFactor(UInt16):
    units = " if"

    def _load(self, data):
        return data / 1000.

    def _save(self, value):
        return int(value * 1000.)


class StrokeCount(UInt32):
    units = " strokes/lap"

    def _load(self, data):
        return data / 10.

    def _save(self, value):
        return int(value * 10.)

class Work(UInt32):
    units = "J"


class Percents(SInt16):
    units = "%"

    def _load(self, data):
        return data / 100.

    def _save(self, value):
        return int(value * 100.)


class Temperature(SInt8):
    units = "°C"


class Oscillation(UInt16):
    units = "mm"

    def _load(self, data):
        return data / 10.

    def _save(self, value):
        return int(value * 10.)


class StancePercents(UInt16):
    units = "%"

    def _load(self, data):
        return data / 100.

    def _save(self, value):
        return int(value * 100.)


class StanceTime(UInt16):
    units = "ms"

    def _load(self, data):
        return data / 10.

    def _save(self, value):
        return int(value * 10.)


class FractionalCadence(Cadence):
    def _load(self, data):
        return data / 128.

    def _save(self, value):
        return int(value * 128.)


class FractionalCycles(UInt8):
    units = " cycles"

    def _load(self, data):
        return data / 128.

    def _save(self, value):
        return int(value * 128.)


class Hemoglobin(UInt16):
    units = " g/dL"

    def _load(self, data):
        return data / 100.

    def _save(self, value):
        return int(value * 100.)


class HemoglobinPercents(UInt16):
    units = "%"

    def _load(self, data):
        return data / 10.

    def _save(self, value):
        return int(value * 10.)


class Accuracy(UInt8):
    units = "m"
