"""Tests for fit.files.filelike — FileLike.create, _apply_mixin, and _validate."""

from __future__ import annotations

from pathlib import Path

import pytest

from fit import FitFile
from fit.files import KNOWN as KNOWN_FILES
from fit.files.activity import ActivityFile
from fit.files.filelike import FileLike
from fit.files.goals import GoalsFile
from fit.messages.common import FileCreator, FileId

# ---------------------------------------------------------------------------
# FileLike.create()
# ---------------------------------------------------------------------------


def test_filelike_create_returns_fitfile(tmp_path: Path) -> None:
    p = tmp_path / "act.fit"
    f = ActivityFile.create(p)
    f.close()
    assert p.exists()


def test_filelike_create_adds_file_id(tmp_path: Path) -> None:
    p = tmp_path / "act.fit"
    with ActivityFile.create(p) as f:
        assert f.file_id is not None
        assert isinstance(f.file_id, FileId)


def test_filelike_create_with_integer_mixin(tmp_path: Path) -> None:
    p = tmp_path / "act2.fit"
    # Pass the integer type code — should look up ActivityFile from KNOWN
    with FileLike.create(p, mixin=4) as f:
        assert f.file_id is not None
        assert f.file_id.filetype == 4


def test_filelike_create_sets_correct_filetype(tmp_path: Path) -> None:
    p = tmp_path / "goals.fit"
    with GoalsFile.create(p) as f:
        assert f.file_id.filetype == 11  # GoalsFile.type == 11


# ---------------------------------------------------------------------------
# _apply_mixin: FitFile subclass path
# ---------------------------------------------------------------------------


def test_apply_mixin_with_fitfile_subclass(tmp_path: Path) -> None:
    """When a registered mixin_cls is a FitFile subclass, it becomes the sole base."""

    class CustomFitFile(FitFile):
        type = 11  # goals file type — valid in File.variants

    original = KNOWN_FILES.get(11)
    KNOWN_FILES[11] = CustomFitFile
    try:
        p = tmp_path / "custom.fit"
        with FitFile.open(p, mode="w") as f:
            f.append(FileId.create(11))
        # Reading back triggers _apply_mixin; __class__ should be a CustomFitFile subclass
        with FitFile.open(p, mode="r") as f:
            assert issubclass(type(f), CustomFitFile)
    finally:
        if original is not None:
            KNOWN_FILES[11] = original
        else:
            del KNOWN_FILES[11]


# ---------------------------------------------------------------------------
# _validate: error paths
# ---------------------------------------------------------------------------


def test_validate_non_message_raises_value_error(tmp_path: Path) -> None:
    p = tmp_path / "v1.fit"
    with FitFile.open(p, mode="w") as f, pytest.raises(ValueError, match="Message"):
        f.append("not a message")  # type: ignore[arg-type]


def test_validate_delete_file_id_from_nonempty_raises_index_error(
    tmp_path: Path,
) -> None:
    p = tmp_path / "v2.fit"
    with FitFile.open(p, mode="w") as f:
        f.append(FileCreator(software_version=1))
        f.append(FileCreator(software_version=2))

    with FitFile.open(p, mode="r") as f:
        # Manually plant a FileId at position 0 so file_id is not None
        file_id = FileId.create(4)
        f.body.insert(0, file_id)
        # Now body has 3 items: [FileId, FC(1), FC(2)]
        # Removing index 0 when len > 1 and file_id present should fail
        with pytest.raises(IndexError, match="file_id"):
            f.remove(0)


def test_validate_update_file_id_of_nonempty_raises_index_error(tmp_path: Path) -> None:
    p = tmp_path / "v3.fit"
    with FitFile.open(p, mode="w") as f:
        f.append(FileCreator(software_version=1))

    with FitFile.open(p, mode="r") as f:
        file_id = FileId.create(4)
        f.body.insert(0, file_id)
        # body: [FileId, FC(1)] - replacing index 0 should fail
        with pytest.raises(IndexError, match="file_id"):
            f[0] = FileCreator(software_version=99)


def test_validate_wrong_record_type_raises_type_error(tmp_path: Path) -> None:
    p = tmp_path / "goals.fit"
    # GoalsFile only allows FileId and Goal — FileCreator is not permitted
    with GoalsFile.create(p) as f, pytest.raises(TypeError, match="doesn't support"):
        f.append(FileCreator(software_version=1))
