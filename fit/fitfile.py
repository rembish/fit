"""FIT file high-level API: FitFile class and file-type registration."""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from copy import copy
from io import UnsupportedOperation
from pathlib import Path
from typing import IO, Any, Union

from fit.files import KNOWN as KNOWN_FILES
from fit.files import FileLike
from fit.io.reader import Reader
from fit.io.writer import Writer
from fit.messages import Message
from fit.structure.body import Body

_PathLike = Union[str, Path]
_OpenArg = Union[str, Path, IO[bytes]]


class FitFile(FileLike):
    """A FIT file object that supports both reading and writing.

    Supports the context-manager protocol and behaves like a mutable list of
    :class:`~fit.messages.Message` objects.

    Do not instantiate directly — use :meth:`open` or
    :meth:`~fit.files.FileLike.create` instead.

    Args:
        ffd: Open binary file descriptor or any readable binary stream.
        body: Pre-parsed :class:`~fit.structure.body.Body` (optional).
    """

    def __init__(self, ffd: Any, body: Body | None = None) -> None:
        self._fd = ffd
        self.body: Body = body or Body()
        self._apply_mixin()

    @classmethod
    def open(cls, filename: _OpenArg, mode: str = "r") -> FitFile:
        """Open a FIT file for reading, writing, or appending.

        *filename* may be a path (``str`` or :class:`pathlib.Path`) or any
        binary-readable stream (e.g. :class:`io.BytesIO`). When a stream is
        passed, *mode* is ignored and the stream is read as-is.

        Args:
            filename: Path to the FIT file or an open binary stream.
            mode: One of ``"r"`` (read), ``"w"`` (write/truncate), or
                ``"a"`` (append). Ignored when *filename* is a stream.

        Returns:
            An open :class:`FitFile` in the requested mode.

        Raises:
            ValueError: If *mode* is not ``"r"``, ``"w"``, or ``"a"``.
        """
        if hasattr(filename, "read"):
            # Already an open stream — read its body and wrap it.
            ffd: IO[bytes] = filename  # type: ignore[assignment]
            return cls(ffd, body=Reader(ffd).body)

        if mode not in ("r", "w", "a"):
            raise ValueError(
                f"mode string must be one of 'r', 'w' or 'a', not {mode!r}"
            )

        path = Path(filename)  # type: ignore[arg-type]
        ffd = open(path, mode="wb" if mode == "w" else "rb")  # type: ignore[assignment]

        body: Body | None = None
        if mode in ("a", "r"):
            body = Reader(ffd).body

        if mode == "a":
            ffd.close()
            ffd = open(path, mode="ab")  # type: ignore[assignment]

        return cls(ffd, body=body)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.name!r}, mode {self.mode[0]!r}>"

    def __del__(self) -> None:
        self.close()

    # Context-manager protocol

    def __enter__(self) -> FitFile:
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()

    # File-like properties

    @property
    def mode(self) -> str:
        """The mode string of the underlying file descriptor (``"rb"`` for streams)."""
        return getattr(self._fd, "mode", "rb")

    @property
    def name(self) -> str:
        """The path/name of the underlying file (``"<stream>"`` for in-memory streams)."""
        return getattr(self._fd, "name", "<stream>")

    @property
    def closed(self) -> bool:
        """``True`` if the file has been closed."""
        return getattr(self._fd, "closed", False)

    def fileno(self) -> int:
        """Return the underlying file descriptor integer.

        Raises:
            UnsupportedOperation: If the stream has no associated file descriptor.
        """
        try:
            return self._fd.fileno()
        except (AttributeError, UnsupportedOperation):
            raise UnsupportedOperation("fileno") from None

    def isatty(self) -> bool:
        """Return ``True`` if the stream is connected to a terminal."""
        return getattr(self._fd, "isatty", lambda: False)()

    def readable(self) -> bool:
        return self.mode[0] in ("r", "a")

    def seekable(self) -> bool:
        return False

    def writable(self) -> bool:
        return self.mode[0] in ("a", "w")

    def write(self) -> None:  # type: ignore[override]
        """Write (or rewrite) the complete FIT file to disk.

        Raises:
            IOError: If the file is not open for writing.
        """
        if not self.writable():
            raise OSError("File not open for writing")
        Writer(self._fd, body=self.body).write()

    def flush(self) -> None:
        """Flush pending data by writing to disk (only when writable)."""
        if self.writable():
            self.write()

    def close(self) -> None:
        """Flush and close the file. No-op if already closed."""
        if self.closed:
            return
        self.flush()
        self._fd.close()

    # Mutable-list interface

    def __getitem__(self, i: int) -> Message:
        return self.body[i]

    def __setitem__(self, i: int, value: Message) -> None:
        self._validate(i, value)
        self.body[i] = value
        self._apply_mixin()

    def __delitem__(self, i: int) -> None:
        self._validate(i)
        del self.body[i]
        self._apply_mixin()

    def __iter__(self) -> Iterator[Message]:
        return iter(self.body)

    def __len__(self) -> int:
        return len(self.body)

    def append(self, value: Message) -> None:
        """Append *value* to the file body after validation."""
        self._validate(len(self), value)
        self.body.append(value)
        self._apply_mixin()

    def extend(self, values: Iterable[Message]) -> None:
        """Append each item in *values* to the file body."""
        for value in values:
            self.append(value)

    def remove(self, i: int) -> None:
        """Remove the message at index *i* after validation."""
        self._validate(i)
        del self.body[i]
        self._apply_mixin()

    def pop(self, i: int = 0) -> Message:
        """Remove and return the message at index *i* after validation."""
        self._validate(i)
        value = self.body.pop(i)
        self._apply_mixin()
        return value

    def copy(self, other: FitFile | None = None) -> Any:
        """Copy the body.

        If *other* is provided, replace this file's body with a copy of
        *other*'s body. Otherwise return a shallow copy of this body.

        Args:
            other: Another :class:`FitFile` to copy from (optional).

        Returns:
            A copy of the body when *other* is ``None``.
        """
        if other is None:
            return copy(self.body)

        assert isinstance(other, FitFile)
        self.body = other.copy()
        self._apply_mixin()
        return None

    def filter_by(self, *message_types: type) -> Iterator[Message]:
        """Yield all messages that are instances of any of *message_types*.

        Args:
            *message_types: One or more message classes to filter by.

        Yields:
            Messages whose type matches any of the given classes.

        Example::

            from fit.messages.activity import Record
            records = list(f.filter_by(Record))
        """
        return (msg for msg in self.body if isinstance(msg, message_types))  # type: ignore[misc]

    def get_messages(self, message_type: str | type) -> Iterator[Message]:
        """Yield all messages matching a type name or class.

        Accepts either a class (like :func:`filter_by`) or a case-insensitive
        string name so callers need not import the message class directly.

        Args:
            message_type: A message class, or a string name such as
                ``"record"``, ``"lap"``, or ``"session"``.

        Yields:
            Matching :class:`~fit.messages.Message` instances.

        Example::

            records = list(f.get_messages("record"))
            laps    = list(f.get_messages("lap"))
        """
        if isinstance(message_type, str):
            name = message_type.lower()
            return (
                msg for msg in self.body if msg.__class__.__name__.lower() == name
            )  # type: ignore[misc]
        return self.filter_by(message_type)

    def merge(self, other: FitFile) -> None:
        """Append all messages from *other* into this file.

        If this file already has a :class:`~fit.messages.common.FileId` record,
        the leading ``FileId`` from *other* (if present) is skipped to avoid
        duplicating the file header.

        Args:
            other: Another :class:`FitFile` whose messages to append.
        """
        from fit.messages.common import FileId

        for i, msg in enumerate(other):
            if i == 0 and self.file_id and isinstance(msg, FileId):
                continue
            self.append(msg)


def register(file_cls: type) -> None:
    """Register a custom :class:`FitFile` subclass in the global file-type table.

    Args:
        file_cls: Must be a :class:`FitFile` subclass with an integer :attr:`type`.

    Raises:
        ValueError: If the preconditions are not met.
    """
    if not issubclass(file_cls, FitFile):
        raise ValueError(f"{file_cls.__name__} should be subclass of FitFile")
    if not isinstance(file_cls.type, int):
        raise ValueError(f"{file_cls.__name__} should have a defined file type")

    KNOWN_FILES[file_cls.type] = file_cls


def _load_plugins() -> None:
    """Discover and register third-party message and file-type plugins.

    Packages can expose custom :class:`~fit.messages.Message` subclasses via
    the ``fit.messages`` entry-point group, and custom :class:`FitFile`
    subclasses via ``fit.files``.  Example in a plugin's ``pyproject.toml``::

        [project.entry-points."fit.messages"]
        my_msg = "mypkg.messages:MyMessage"

        [project.entry-points."fit.files"]
        my_file = "mypkg.files:MyFile"
    """
    from importlib.metadata import entry_points

    from fit.messages import register as register_message

    msg_eps = entry_points(group="fit.messages")  # type: ignore[call-arg]
    file_eps = entry_points(group="fit.files")  # type: ignore[call-arg]

    for ep in msg_eps:
        register_message(ep.load())  # type: ignore[attr-defined]

    for ep in file_eps:
        register(ep.load())  # type: ignore[attr-defined]


_load_plugins()
