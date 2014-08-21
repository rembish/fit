from fit.messages import Message


class DeviceSettings(Message):
    msg_type = 2


class UserProfile(Message):
    msg_type = 3


class HrmProfile(Message):
    msg_type = 4


class SdmProfile(Message):
    msg_type = 5


class BikeProfile(Message):
    msg_type = 6
