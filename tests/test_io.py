"""Tests for fit.io (Reader/Writer) and FitFile high-level API."""

from __future__ import annotations

import struct
from io import BytesIO
from pathlib import Path

import pytest

import fit
from fit import FitFile
from fit.exceptions import HeaderFormatError
from fit.io.reader import Reader
from fit.io.writer import Writer
from fit.messages.common import FileCreator, FileId
from fit.structure.body import Body
from fit.structure.crc import compute_crc

from .conftest import make_fit_bytes

# ---------------------------------------------------------------------------
# Reader
# ---------------------------------------------------------------------------


def test_reader_reads_empty_file() -> None:
    reader = Reader(BytesIO(make_fit_bytes()))
    assert reader.header.valid
    assert len(reader.body) == 0


def test_reader_header_size() -> None:
    assert Reader(BytesIO(make_fit_bytes())).header.size == 14


def test_reader_header_versions() -> None:
    reader = Reader(BytesIO(make_fit_bytes()))
    assert reader.header.protocol_version == 16
    assert reader.header.profile_version == 1005


def test_reader_crc_is_set() -> None:
    assert Reader(BytesIO(make_fit_bytes())).crc.value is not None


def test_reader_bad_magic_raises() -> None:
    bad = struct.pack("<BBHL4s", 12, 16, 1005, 0, b"NFIT")
    bad += struct.pack("<H", compute_crc(b""))
    with pytest.raises(HeaderFormatError):
        _ = Reader(BytesIO(bad)).header


def test_reader_wrong_header_size_raises() -> None:
    bad = struct.pack("<BBHL4s", 99, 16, 1005, 0, b".FIT")
    with pytest.raises(HeaderFormatError):
        _ = Reader(BytesIO(bad)).header


def test_reader_from_file_path(fit_path: Path) -> None:
    with open(fit_path, "rb") as f:
        assert Reader(f).header.valid


def test_reader_repr() -> None:
    r = Reader(BytesIO(make_fit_bytes()))
    assert "Reader" in repr(r)


# ---------------------------------------------------------------------------
# Writer
# ---------------------------------------------------------------------------


def test_writer_empty_body_is_readable(tmp_path: Path) -> None:
    p = tmp_path / "out.fit"
    with open(p, "wb") as f:
        Writer(f, body=Body()).write()
    with open(p, "rb") as f:
        assert Reader(f).header.valid
        assert len(Reader(f).body) == 0


def test_writer_round_trip_with_message(tmp_path: Path) -> None:
    p = tmp_path / "rt.fit"
    body = Body()
    body.append(FileCreator(software_version=42))

    with open(p, "wb") as f:
        Writer(f, body=body).write()

    with open(p, "rb") as f:
        loaded = Reader(f).body

    assert len(loaded) == 1
    assert isinstance(loaded[0], FileCreator)
    assert loaded[0].software_version == 42


# ---------------------------------------------------------------------------
# FitFile
# ---------------------------------------------------------------------------


def test_fitfile_open_read_empty(fit_path: Path) -> None:
    with FitFile.open(fit_path, mode="r") as f:
        assert len(f) == 0


def test_fitfile_open_write_and_read_back(tmp_path: Path) -> None:
    p = tmp_path / "new.fit"
    with FitFile.open(p, mode="w") as f:
        f.append(FileCreator(software_version=7))

    with FitFile.open(p, mode="r") as f:
        assert len(f) == 1
        assert isinstance(f[0], FileCreator)
        assert f[0].software_version == 7


def test_fitfile_context_manager_closes(fit_path: Path) -> None:
    with FitFile.open(fit_path, mode="r") as f:
        assert not f.closed
    assert f.closed


def test_fitfile_invalid_mode_raises(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="mode"):
        FitFile.open(tmp_path / "x.fit", mode="x")


def test_fitfile_accepts_path_object(fit_path: Path) -> None:
    with FitFile.open(fit_path) as f:
        assert not f.closed


def test_fitfile_open_stream(fit_stream: BytesIO) -> None:
    f = FitFile.open(fit_stream)
    assert len(f) == 0


def test_fitfile_stream_mode_is_rb(fit_stream: BytesIO) -> None:
    assert FitFile.open(fit_stream).mode == "rb"


def test_fitfile_stream_name_is_stream(fit_stream: BytesIO) -> None:
    assert FitFile.open(fit_stream).name == "<stream>"


def test_fitfile_filter_by_returns_matching(tmp_path: Path) -> None:
    p = tmp_path / "filter.fit"
    with FitFile.open(p, mode="w") as f:
        f.append(FileCreator(software_version=1))
        f.append(FileCreator(software_version=2))

    with FitFile.open(p, mode="r") as f:
        results = list(f.filter_by(FileCreator))
    assert len(results) == 2
    assert all(isinstance(r, FileCreator) for r in results)


def test_fitfile_filter_by_no_match(tmp_path: Path) -> None:
    p = tmp_path / "filter2.fit"
    with FitFile.open(p, mode="w") as f:
        f.append(FileCreator(software_version=1))

    with FitFile.open(p, mode="r") as f:
        assert list(f.filter_by(FileId)) == []


def test_fitfile_copy_returns_body() -> None:
    f = FitFile.open(BytesIO(make_fit_bytes()))
    body_copy = f.copy()
    assert len(body_copy) == 0


def test_fitfile_copy_from_empty_source(tmp_path: Path) -> None:
    """copy(other) must work even when other has len == 0."""
    src = FitFile.open(BytesIO(make_fit_bytes()))
    dst_path = tmp_path / "dst.fit"
    with FitFile.open(dst_path, mode="w") as dst:
        dst.copy(src)


def test_fitfile_remove_by_index(tmp_path: Path) -> None:
    p = tmp_path / "remove.fit"
    with FitFile.open(p, mode="w") as f:
        f.append(FileCreator(software_version=1))
        f.append(FileCreator(software_version=2))

    with FitFile.open(p, mode="r") as f:
        assert len(f) == 2
        f.remove(1)
        assert len(f) == 1


def test_fitfile_extend_with_list(tmp_path: Path) -> None:
    p = tmp_path / "extend.fit"
    msgs = [FileCreator(software_version=i) for i in range(3)]
    with FitFile.open(p, mode="w") as f:
        f.extend(msgs)

    with FitFile.open(p, mode="r") as f:
        assert len(f) == 3


def test_fitfile_version_is_exported() -> None:
    assert fit.__version__ == "0.5.1"


def test_get_messages_by_class(tmp_path: Path) -> None:
    p = tmp_path / "gm.fit"
    with FitFile.open(p, mode="w") as f:
        f.append(FileCreator(software_version=1))
        f.append(FileCreator(software_version=2))

    with FitFile.open(p, mode="r") as f:
        results = list(f.get_messages(FileCreator))
    assert len(results) == 2


def test_get_messages_by_name(tmp_path: Path) -> None:
    p = tmp_path / "gm2.fit"
    with FitFile.open(p, mode="w") as f:
        f.append(FileCreator(software_version=3))

    with FitFile.open(p, mode="r") as f:
        results = list(f.get_messages("filecreator"))
    assert len(results) == 1
    assert results[0].software_version == 3


def test_get_messages_name_case_insensitive(tmp_path: Path) -> None:
    p = tmp_path / "gm3.fit"
    with FitFile.open(p, mode="w") as f:
        f.append(FileCreator(software_version=1))

    with FitFile.open(p, mode="r") as f:
        assert list(f.get_messages("FileCreator")) == list(
            f.get_messages("filecreator")
        )


def test_merge_appends_messages(tmp_path: Path) -> None:
    src = tmp_path / "src.fit"
    dst = tmp_path / "dst.fit"

    with FitFile.open(src, mode="w") as f:
        f.append(FileCreator(software_version=1))
        f.append(FileCreator(software_version=2))

    with FitFile.open(dst, mode="w") as f:
        f.append(FileCreator(software_version=0))

    with FitFile.open(src, mode="r") as src_f, FitFile.open(dst, mode="r") as dst_f:
        dst_f.merge(src_f)
        assert len(dst_f) == 3


def test_merge_skips_duplicate_file_id(tmp_path: Path) -> None:
    """merge() skips the source FileId when destination already has one."""
    src = tmp_path / "src.fit"
    dst = tmp_path / "dst.fit"

    with FitFile.open(src, mode="w") as f:
        f.append(FileId.create(4))
        f.append(FileCreator(software_version=1))

    with FitFile.open(dst, mode="w") as f:
        f.append(FileId.create(4))

    with FitFile.open(src, mode="r") as src_f, FitFile.open(dst, mode="r") as dst_f:
        dst_f.merge(src_f)
        file_ids = list(dst_f.filter_by(FileId))

    assert len(file_ids) == 1
