from fit.messages import Message
from fit.types.additional import Degrees, Distance
from fit.types.extended import Sport, CourseCapabilities, MessageIndex, \
    DateTime
from fit.types.extended import CoursePoint as CoursePointField
from fit.types.general import String


class Course(Message):
    msg_type = 31

    sport = Sport(4)
    name = String(5)
    capabilities = CourseCapabilities(6)


class CoursePoint(Message):
    msg_type = 32

    message_index = MessageIndex(254)
    timestamp = DateTime(1)
    position_lat = Degrees(2)
    position_long = Degrees(3)
    distance = Distance(4)
    type = CoursePointField(5)
    name = String(6)
