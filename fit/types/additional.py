# coding=utf-8
from fit.types.general import SInt32, UInt16, UInt32, UInt8, SInt16, SInt8
from fit.types.mixins import ScaleMixin


def degrees(number):
    return SInt32(number, units="°") * (2 ** 31 / 180.)
