from fit.message import Message


class Software(Message):
    msg_type = 35


class SlaveDevice(Message):
    msg_type = 106


class Capabilities(Message):
    msg_type = 1


class FileCapabilities(Message):
    msg_type = 37


class MesgCapabilities(Message):
    msg_type = 38


class FieldCapabilities(Message):
    msg_type = 39
