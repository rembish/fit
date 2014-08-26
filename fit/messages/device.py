from fit.messages import Message
from fit.types.extended import MessageIndex, Manufacturer, GarminProduct, \
    SportBits0, WorkoutCapabilities, ConnectivityCapabilities, File, \
    FileFlags, MesgNum, MesgCount
from fit.types.general import String, UInt8Z, UInt16, UInt32, UInt8


class Software(Message):
    msg_type = 35

    message_index = MessageIndex(254)
    version = UInt16(3) * 100
    part_number = String(5)


class SlaveDevice(Message):
    msg_type = 106

    manufacturer = Manufacturer(0)
    product = GarminProduct(1)


class Capabilities(Message):
    msg_type = 1

    languages = UInt8Z(0)  # array
    sports = SportBits0(1)  # array
    workouts_supported = WorkoutCapabilities(21)
    connectivity_supported = ConnectivityCapabilities(23)


class FileCapabilities(Message):
    msg_type = 37

    message_index = MessageIndex(254)
    type = File(0)
    flags = FileFlags(1)
    directory = String(2)
    max_count = UInt16(3)
    max_size = UInt32(4)


class MesgCapabilities(Message):
    msg_type = 38

    message_index = MessageIndex(254)
    file = File(0)
    mesg_num = MesgNum(1)
    count_type = MesgCount(2)
    count = UInt16(3)


class FieldCapabilities(Message):
    msg_type = 39

    message_index = MessageIndex(254)
    file = File(0)
    mesg_num = MesgNum(1)
    field_num = UInt8(2)
    count = UInt16(3)
