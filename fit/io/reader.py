"""FIT file reader: parses header, body, and CRC from a binary stream."""

from __future__ import annotations

from io import UnsupportedOperation
from os import SEEK_END
from typing import IO

from fit.exceptions import BodyFormatError, CrcFormatError, HeaderFormatError
from fit.structure.body import Body
from fit.structure.crc import Crc, compute_crc
from fit.structure.header import Header

__all__ = ["Reader"]


class Reader:
    """Reads and validates a FIT file from a binary stream.

    Parsing is lazy: :attr:`header`, :attr:`body`, and :attr:`crc` are each
    parsed on first access.

    Args:
        ffd: Open binary-mode file object (``"rb"`` or any readable binary stream).
    """

    def __init__(self, ffd: IO[bytes]) -> None:
        self._fd: IO[bytes] = ffd

        self._header: Header = Header()
        self._body: Body = Body()
        self._crc: Crc = Crc()

        try:
            from os import fstat

            self.file_size: int = fstat(self._fd.fileno()).st_size  # type: ignore[arg-type]
        except (UnsupportedOperation, AttributeError):
            self._fd.seek(0, SEEK_END)
            self.file_size = self._fd.tell()
            self._fd.seek(0)

        self.header_chunk: bytes = b""

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} "
            f"header={self.header!r} body={self.body!r} crc={self.crc!r}>"
        )

    @property
    def header(self) -> Header:
        """Parse and return the FIT file header (cached after first access).

        Raises:
            HeaderFormatError: If the header is malformed or the magic is wrong.
        """
        if self._header:
            return self._header

        self._fd.seek(0)

        header_size = self._fd.read(1)[0]
        if header_size not in (12, 14):
            raise HeaderFormatError(f"Strange size: {header_size} bytes")

        rest = self._fd.read(header_size - 1)
        if len(rest) != header_size - 1:
            raise HeaderFormatError(
                f"Can't read {header_size} bytes, "
                f"read {len(rest) + 1} bytes instead"
            )

        header_bytes = bytes([header_size]) + rest
        self.header_chunk = header_bytes
        self._header.read(header_bytes)

        if not self._header.valid:
            raise HeaderFormatError("Not a FIT file")

        if self._header.total_size != self.file_size:
            raise HeaderFormatError(
                f"File size should be {self._header.total_size} bytes, "
                f"but is actually {self.file_size} bytes"
            )

        return self._header

    @property
    def body(self) -> Body:
        """Parse and return the FIT file body (cached after first access).

        Raises:
            BodyFormatError: If the body cannot be fully read or the CRC fails.
        """
        if not self._body:
            self._fd.seek(self.header.size)  # type: ignore[arg-type]

            body_bytes = self._fd.read(self.header.data_size)  # type: ignore[arg-type]
            if len(body_bytes) != self.header.data_size:
                raise BodyFormatError(
                    f"Can't read {self.header.data_size} bytes, "
                    f"read {len(body_bytes)} bytes instead"
                )

            header_prefix = b"" if self.header.crc.value else self.header_chunk
            if not self.crc.check(header_prefix + body_bytes):
                raise BodyFormatError(
                    f"Invalid CRC {compute_crc(body_bytes):#x}, "
                    f"should be {self.crc.value:#x}"
                )

            self._body.read(body_bytes)
        return self._body

    @property
    def crc(self) -> Crc:
        """Parse and return the trailing CRC field (cached after first access).

        Raises:
            CrcFormatError: If the CRC bytes cannot be read.
        """
        if not self._crc:
            self._fd.seek(self.header.size + self.header.data_size)  # type: ignore[operator]

            chunk = self._fd.read(self._crc.size)
            if len(chunk) != self._crc.size:
                raise CrcFormatError(
                    f"Can't read {self._crc.size} bytes, "
                    f"read {len(chunk)} bytes instead"
                )

            self._crc.read(chunk)
        return self._crc
