"""Module docstring."""

from __future__ import annotations

from fit.messages.message import Message
from fit.types.extended import MessageIndex
from fit.types.general import Byte, UInt16, UInt32


class MemoGlob(Message):
    msg_type = 145

    part_index = UInt32(250)
    memo = Byte(0)
    message_number = UInt16(1)
    message_index = MessageIndex(2)
