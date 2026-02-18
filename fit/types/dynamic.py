"""Dynamic (sub-field) type: a field whose interpretation depends on another field."""

from __future__ import annotations

from typing import IO, Any, Callable

from fit.types.base import Type

__all__ = ["Dynamic", "SubField"]


class Dynamic(Type):
    """A FIT field whose active sub-type is determined by a sibling field's value.

    For example, ``product`` may be interpreted as ``garmin_product`` when
    ``manufacturer`` equals ``"garmin"``.

    Args:
        base: The underlying :class:`~fit.types.Type` used for raw I/O.
        referred_to: Name of the sibling field that selects the active sub-field.
        **kwargs: Mapping of referred-field value(s) → :class:`SubField`.
            Keys may be a single value, or a list/tuple/set of values.
    """

    def __init__(
        self,
        base: Type,
        referred_to: str,
        **kwargs: SubField,
    ) -> None:
        super().__init__(base.number, size=base.size)
        self.base: Type = base
        self.referred: str = referred_to
        self.variants: dict[Any, SubField] = kwargs

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} of {self.base!r}>"

    @property
    def type(self) -> int | None:  # type: ignore[override]
        return self.base.type

    def read(self, read_buffer: IO[bytes], architecture: str = "<") -> Any:
        return self.base.read(read_buffer, architecture=architecture)

    def write(self, value: Any) -> bytes:
        return self.base.write(value)

    def get_subfield(self, referred_value: Any) -> SubField | None:
        """Return the :class:`SubField` matching *referred_value*, or ``None``."""
        for keys, subfield in self.variants.items():
            if not isinstance(keys, (list, tuple, set, frozenset)):
                keys = (keys,)
            if referred_value in keys:
                return subfield
        return None


class SubField:
    """A named interpretation of a :class:`Dynamic` field's raw value.

    Args:
        field_name: Attribute name exposed on the message.
        field_type: Optional override type class used when reading/writing.
        **kwargs: Additional constructor arguments forwarded to *field_type*.
    """

    def __init__(
        self,
        field_name: str,
        field_type: type | Callable[..., Any] | None = None,
        **kwargs: Any,
    ) -> None:
        self.name: str = field_name
        self.type: type | Callable[..., Any] | None = field_type
        self.kwargs: dict[str, Any] = kwargs
