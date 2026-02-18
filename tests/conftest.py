"""Shared pytest fixtures for the fit test suite."""

from __future__ import annotations

import struct
from io import BytesIO
from pathlib import Path

import pytest

from fit.structure.crc import compute_crc


def make_fit_bytes(body: bytes = b"") -> bytes:
    """Build a minimal valid 14-byte-header FIT file in memory.

    Args:
        body: Pre-serialised body bytes.

    Returns:
        Complete FIT file bytes (header + body + trailing CRC).
    """
    header_body = struct.pack("<BBHL4s", 14, 16, 1005, len(body), b".FIT")
    header_crc = struct.pack("<H", compute_crc(header_body))
    header = header_body + header_crc
    trailing_crc = struct.pack("<H", compute_crc(body))
    return header + body + trailing_crc


@pytest.fixture()
def fit_bytes() -> bytes:
    """A valid empty FIT file with no body messages."""
    return make_fit_bytes()


@pytest.fixture()
def fit_path(tmp_path: Path, fit_bytes: bytes) -> Path:
    """Write an empty FIT file to a temporary path and return it."""
    p = tmp_path / "empty.fit"
    p.write_bytes(fit_bytes)
    return p


@pytest.fixture()
def fit_stream(fit_bytes: bytes) -> BytesIO:
    """An in-memory BytesIO stream containing a valid empty FIT file."""
    return BytesIO(fit_bytes)
