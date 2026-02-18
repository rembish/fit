"""Module docstring."""

from __future__ import annotations

from fit.messages.message import Message
from fit.types.extended import (
    Bool,
    DateTime,
    GoalRecurrence,
    MessageIndex,
    Sport,
    SubSport,
)
from fit.types.extended import Goal as GoalField
from fit.types.general import UInt16, UInt32


class Goal(Message):
    msg_type = 15

    message_index = MessageIndex(254)
    sport = Sport(0)
    sub_sport = SubSport(1)
    start_date = DateTime(2)
    end_date = DateTime(3)
    type = GoalField(4)
    value = UInt32(5)
    repeat = Bool(6)
    target_value = UInt32(7)
    recurrence = GoalRecurrence(8)
    recurrence_value = UInt16(9)
    enabled = Bool(10)
