from fit.message import Message
from fit.types.additional import TimerTime, Distance, Calories
from fit.types.extended import MessageIndex, DateTime, Sport
from fit.types.general import UInt16


class Totals(Message):
    msg_type = 33

    message_index = MessageIndex(254)
    timestamp = DateTime(253)
    timer_time = TimerTime(0)
    distance = Distance(1)
    calories = Calories(2)
    sport = Sport(3)
    elapsed_time = TimerTime(4)
    sessions = UInt16(5)
    active_time = TimerTime(6)
