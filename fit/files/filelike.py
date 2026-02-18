"""FIT file-type mixin classes and the global file-type registry."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Type  # noqa: UP035

from fit.messages import Message
from fit.messages.common import FileId
from fit.utils import get_known

if TYPE_CHECKING:
    from fit import FitFile

__all__ = ["KNOWN", "FileLike"]


class FileLike:
    """Base mixin for typed FIT files.

    Subclasses set :attr:`type` to the integer file-type code and may restrict
    :attr:`record_types` to a subset of allowed message classes.
    """

    body: list[Any] = []
    type: int | None = None
    record_types: frozenset[Type[Any]] = frozenset((Message,))  # noqa: UP006

    @property
    def file_id(self) -> FileId | None:
        """The first message if it is a :class:`~fit.messages.common.FileId`, else ``None``."""
        if len(self.body) and isinstance(self.body[0], FileId):
            return self.body[0]
        return None

    @classmethod
    def create(cls, filename: Any, mixin: Any = None) -> FitFile:
        """Create a new writable FIT file with a :class:`~fit.messages.common.FileId` header.

        Args:
            filename: Path to the file to create (``str`` or :class:`pathlib.Path`).
            mixin: File-type class or integer type code. Defaults to *cls*.

        Returns:
            An open :class:`~fit.FitFile` ready for writing.
        """
        from fit import FitFile

        instance = FitFile.open(filename, mode="w")

        mixin = mixin or cls
        if not mixin:
            return instance

        if isinstance(mixin, int):
            mixin = KNOWN[mixin]

        instance.append(FileId.create(mixin.type))
        return instance

    def _apply_mixin(self) -> None:
        """Dynamically update ``self.__class__`` based on the file-type in :attr:`file_id`."""
        from fit import FitFile

        mcs = [FitFile]
        if self.file_id:
            mixin_cls = KNOWN.get(self.file_id.filetype)
            if mixin_cls:
                if issubclass(mixin_cls, FitFile):
                    mcs = [mixin_cls]  # type: ignore[list-item]
                else:
                    mcs.append(mixin_cls)  # type: ignore[arg-type]
        self.__class__ = type(mcs[-1].__name__, tuple(mcs), {})

    def _validate(self, i: int, value: Any | None = None) -> None:
        """Validate an insert/update/delete operation on the body list.

        Args:
            i: Index being modified.
            value: The new message (``None`` for deletion).

        Raises:
            ValueError: If *value* is not a :class:`~fit.messages.Message`.
            IndexError: If the operation would corrupt the file-id record.
            TypeError: If *value* is not a permitted record type for this file.
        """
        if value and not isinstance(value, Message):
            raise ValueError(f"Item should be instance of {Message.__name__} type")

        if not value:  # deletion
            if i == 0 and len(self.body) > 1 and self.file_id:
                raise IndexError("Can't remove file_id record from a non-empty file")
        else:  # insertion or update
            if i == 0 and len(self.body) > 1 and self.file_id:
                raise IndexError("Can't update file_id record of a non-empty file")
            elif not isinstance(value, tuple(self.record_types)):
                raise TypeError(
                    f"{self.__class__.__name__} doesn't support "
                    f"{value.__class__.__name__} records"
                )


KNOWN: dict[Any, type[FileLike]] = get_known("fit.files", FileLike)
