from fit.messages import Message
from fit.types.extended import Sport, CourseCapabilities, MessageIndex, \
    DateTime
from fit.types.extended import CoursePoint as CoursePointField
from fit.types.general import String, UInt32
from fit.types.helpers import degrees


class Course(Message):
    msg_type = 31

    sport = Sport(4)
    name = String(5)
    capabilities = CourseCapabilities(6)


class CoursePoint(Message):
    msg_type = 32

    message_index = MessageIndex(254)
    timestamp = DateTime(1)
    position_lat = degrees(2)
    position_long = degrees(3)
    distance = UInt32(4, units="m") * 100
    type = CoursePointField(5)
    name = String(6)
