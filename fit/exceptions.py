"""Custom exceptions for the FIT file I/O library."""

from __future__ import annotations

__all__ = [
    "BodyFormatError",
    "CrcFormatError",
    "FormatError",
    "HeaderFormatError",
]


class FormatError(Exception):
    """Base exception for all FIT format errors."""


class HeaderFormatError(FormatError):
    """Raised when the FIT file header is malformed or unrecognised."""


class BodyFormatError(FormatError):
    """Raised when the FIT file body is malformed."""


class CrcFormatError(FormatError):
    """Raised when the FIT file CRC section cannot be read."""
