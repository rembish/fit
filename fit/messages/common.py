"""Common FIT messages: FileId and FileCreator."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from fit.messages.message import Message
from fit.types.dynamic import Dynamic, SubField
from fit.types.extended import DateTime, File, GarminProduct, Manufacturer
from fit.types.general import UInt8, UInt16, UInt32Z

__all__ = ["FileCreator", "FileId"]


class FileId(Message):
    """FIT message 0: identifies the type and origin of a FIT file."""

    msg_type = 0

    type = File(0)
    manufacturer = Manufacturer(1)
    product = Dynamic(
        UInt16(2),
        referred_to="manufacturer",
        garmin=SubField("garmin_product", GarminProduct),
        dynastream=SubField("garmin_product", GarminProduct),
        dynastream_oem=SubField("garmin_product", GarminProduct),
    )
    serial_number = UInt32Z(3)
    time_created = DateTime(4)
    number = UInt16(5)

    @property
    def filetype(self) -> int:
        """Return the raw integer file-type code from the :attr:`type` field."""
        return self._meta.model[0]._save(self.type)

    @classmethod
    def create(cls, file_type: int, **data: Any) -> FileId:
        """Construct a :class:`FileId` with sensible default values.

        Args:
            file_type: Integer FIT file type (e.g. ``4`` for activity).
            **data: Field overrides passed to the constructor.

        Returns:
            A populated :class:`FileId` instance.
        """
        attributes: dict[str, Any] = {
            "serial_number": 0xDEADBEEF,
            "time_created": datetime.now(),
            "manufacturer": Manufacturer.known[1],
            "garmin_product": GarminProduct.known[65534],
            "type": File.variants[file_type],
        }
        attributes.update(data)
        return cls(**attributes)


class FileCreator(Message):
    """FIT message 49: records the software and hardware versions of the creator."""

    msg_type = 49

    software_version = UInt16(0)
    hardware_version = UInt8(1)
