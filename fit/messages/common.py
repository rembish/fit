from datetime import datetime

from fit.messages import Message
from fit.types.additional import Version
from fit.types.dynamic import Dynamic
from fit.types.general import UInt32Z, UInt16, UInt8
from fit.types.extended import DateTime, Manufacturer, File, GarminProduct


class FileId(Message):
    msg_type = 0

    serial_number = UInt32Z(3)
    time_created = DateTime(4)
    manufacturer = Manufacturer(1)
    product = Dynamic(
        UInt16(2),
        manufacturer={
            ("garmin", "dynastream", "dynastream_oem"): GarminProduct
        }
    )
    number = UInt16(5)
    type = File(0)

    @property
    def filetype(self):
        return self._meta.model[0]._save(self.type)

    @classmethod
    def create(cls, file_type, **data):
        attributes = {
            'serial_number': 0xDEADBEAF,
            'time_created': datetime.now(),
            'manufacturer': Manufacturer.known[1],
            'product': GarminProduct.known[65534],
            'type': File.variants[file_type]
        }
        attributes.update(data)

        return cls(**attributes)


class FileCreator(Message):
    msg_type = 49

    software_version = Version(0)
    hardware_version = UInt8(1)
