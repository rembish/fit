"""Module docstring."""

from __future__ import annotations

from fit.messages.message import Message
from fit.types.extended import (
    Bool,
    DateTime,
    GarminProduct,
    LocalDateTime,
    Manufacturer,
)
from fit.types.extended import Schedule as ScheduleField
from fit.types.general import UInt32Z


class Schedule(Message):
    msg_type = 28

    manufacturer = Manufacturer(0)
    product = GarminProduct(1)
    serial_number = UInt32Z(2)
    time_created = DateTime(3)
    completed = Bool(4)
    type = ScheduleField(5)
    scheduled_time = LocalDateTime(6)
