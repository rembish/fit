"""Array type: a fixed-count sequence of identical FIT base-type values."""

from __future__ import annotations

from typing import IO, Any

from fit.types.base import Type

__all__ = ["Array"]


class Array(Type):
    """A FIT field that contains a fixed number of repeated values.

    The element count is derived from the total field :attr:`size` and the
    size of :attr:`value_type`.

    Args:
        value_type: The :class:`~fit.types.Type` instance used for each element.
        size: Total byte length of the array field (optional; set later by
            the definition reader).
    """

    def __init__(self, value_type: Type, size: int | None = None) -> None:
        super().__init__(value_type.number, size=size)
        self.value_type: Type = value_type

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.value_type!r}x{self.count}>"

    @property
    def count(self) -> int:
        """Number of elements in the array."""
        return self.size // self.value_type.size

    def read(self, read_buffer: IO[bytes], architecture: str = "<") -> list[Any]:
        """Read :attr:`count` elements from *read_buffer*.

        Returns:
            List of decoded values.
        """
        return [
            self.value_type.read(read_buffer, architecture=architecture)
            for _ in range(self.count)
        ]

    def write(self, values: Any) -> bytes:
        """Pack all *values* into bytes.

        Args:
            values: Sequence of Python values compatible with :attr:`value_type`.

        Returns:
            Concatenated packed bytes for every element.
        """
        return b"".join(self.value_type.write(value) for value in values)
