from fit.message import Message
from fit.type.general import UInt32Z, UInt16, UInt8
from fit.type.extended import DateTime, Manufacturer, File


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
