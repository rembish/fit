"""Generic (unknown) FIT message type."""

from __future__ import annotations

from fit.messages.message import Message
from fit.types.extended import DateTime, MessageIndex
from fit.types.general import UInt32

__all__ = ["GenericMessage"]


class GenericMessage(Message):
    """Fallback message class for unrecognised FIT message numbers.

    Fields common to many message types (timestamp, message_index, part_index)
    are declared so they are always accessible.
    """

    timestamp = DateTime(253)
    message_index = MessageIndex(254)
    part_index = UInt32(250)

    def __init__(self, definition: object) -> None:
        super().__init__(definition)
        self.msg_type: int | None = None
