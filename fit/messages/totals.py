from fit.messages import Message
from fit.types.extended import MessageIndex, DateTime, Sport
from fit.types.general import UInt16, UInt32


class Totals(Message):
    msg_type = 33

    message_index = MessageIndex(254)
    timestamp = DateTime(253) * "s"
    timer_time = UInt32(0) * "s"
    distance = UInt32(1) * "m"
    calories = UInt32(2) * "kcal"
    sport = Sport(3)
    elapsed_time = UInt32(4) * "s"
    sessions = UInt16(5)
    active_time = UInt32(6) * "s"
