"""FIT file header parsing and serialisation."""

from __future__ import annotations

from struct import Struct

from fit.exceptions import BodyFormatError
from fit.structure.crc import Crc, compute_crc

__all__ = ["Header"]

_FIT_MAGIC = b".FIT"


class Header:
    """The FIT file header (12 or 14 bytes).

    The 14-byte variant includes a two-byte CRC over the first 12 bytes.

    Attributes:
        size: Header size in bytes (``None`` until read/written).
        data_type: Four-byte magic ``b".FIT"``.
        data_size: Number of bytes in the file body.
        crc: The header CRC field.
        protocol_version: FIT protocol version encoded as an integer.
        profile_version: FIT profile version encoded as an integer.
    """

    def __init__(self) -> None:
        self._format: Struct = Struct("<BBHL4s")

        self.size: int | None = None
        self.data_type: bytes = _FIT_MAGIC
        self.data_size: int | None = None
        self.crc: Crc = Crc()

        self.protocol_version: int = 16
        self.profile_version: int = 1005

    def __bool__(self) -> bool:
        return self.size is not None

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} "
            f"protocol={self.protocol_version} "
            f"profile={self.profile_version} "
            f"crc={self.crc!r}>"
        )

    @property
    def total_size(self) -> int:
        """Total file size: header + body + trailing CRC."""
        assert self.size is not None and self.data_size is not None
        return self.size + self.data_size + self.crc.size

    @property
    def valid(self) -> bool:
        """``True`` when the magic bytes identify a FIT file."""
        return self.data_type == _FIT_MAGIC

    def read(self, chunk: bytes) -> None:
        """Parse a 12- or 14-byte header from *chunk*.

        Args:
            chunk: Raw header bytes (12 or 14 bytes).

        Raises:
            BodyFormatError: If the 14-byte header CRC is present and invalid.
        """
        (
            self.size,
            self.protocol_version,
            self.profile_version,
            self.data_size,
            self.data_type,
        ) = self._format.unpack(chunk[:12])

        if len(chunk) == 14:
            self.crc.read(chunk[12:])

            if self.crc.value and not self.crc.check(chunk[:12]):
                raise BodyFormatError(
                    f"Invalid CRC {compute_crc(chunk[:12]):#x}, "
                    f"should be {self.crc.value:#x}"
                )

    def write(self) -> bytes:
        """Serialise the header to 14 bytes (including a freshly computed CRC).

        Returns:
            14 packed bytes ready to write to a file.
        """
        self.size = 14
        chunk = self._format.pack(
            self.size,
            self.protocol_version,
            self.profile_version,
            self.data_size,
            self.data_type,
        )
        self.crc.value = compute_crc(chunk)
        return chunk + self.crc.write()
