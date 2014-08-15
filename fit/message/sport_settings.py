from fit.message import Message


class ZonesTarget(Message):
    msg_type = 7


class Sport(Message):
    msg_type = 12


class HrZone(Message):
    msg_type = 8


class SpeedZone(Message):
    msg_type = 53


class CadenceZone(Message):
    msg_type = 131


class PowerZone(Message):
    msg_type = 9


class MetZone(Message):
    msg_type = 10
