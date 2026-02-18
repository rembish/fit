"""FIT file writer: serialises a Body to a binary stream."""

from __future__ import annotations

from typing import IO

from fit.structure.body import Body
from fit.structure.crc import Crc, compute_crc
from fit.structure.header import Header

__all__ = ["Writer"]


class Writer:
    """Writes a :class:`~fit.structure.body.Body` to a binary file stream.

    Args:
        ffd: Open binary file object (``"wb"`` or ``"ab"``).
        body: The :class:`~fit.structure.body.Body` to serialise.
            If ``None``, an empty body is used.
    """

    def __init__(self, ffd: IO[bytes], body: Body | None = None) -> None:
        self._fd: IO[bytes] = ffd
        self.header: Header = Header()
        self.body: Body = body or Body()
        self.crc: Crc = Crc()

    def __repr__(self) -> str:
        if not self.header or self.crc:
            self._prepare()
        return (
            f"<{self.__class__.__name__} "
            f"header={self.header!r} body={self.body!r} crc={self.crc!r}>"
        )

    def _prepare(self) -> bytes:
        """Serialise the body, update the header data size and compute the CRC.

        Returns:
            Packed body bytes.
        """
        chunk = self.body.write()
        self.header.data_size = len(chunk)
        self.crc.value = compute_crc(chunk)
        return chunk

    def write(self) -> None:
        """Write the complete FIT file (header + body + CRC) to :attr:`_fd`.

        The stream is seeked to the beginning and truncated before writing.
        """
        chunk = self._prepare()

        self._fd.seek(0)
        self._fd.truncate()

        self._fd.write(self.header.write())
        self._fd.write(chunk)
        self._fd.write(self.crc.write())
