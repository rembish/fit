# Changelog

## 0.5.0 (2026-02-18)

### Python version

- Drop Python 2 support; require Python ≥ 3.9
- Drop compatibility shims for `long`, `unicode`, `super(Cls, self)`, `__nonzero__`, `raise T, V, TB`

### New API

- `FitFile.open()` accepts `str`, `pathlib.Path`, or any binary-readable stream
- `FitFile.open()` supports `mode="r"`, `"w"`, and `"a"`; context-manager protocol (`with ... as f:`)
- `FitFile.filter_by(*types)` — yield messages by class
- `FitFile.get_messages(type_or_name)` — yield messages by class or case-insensitive string name
- `FitFile.merge(other)` — append all messages from another `FitFile`, skipping a duplicate `FileId`
- `FitFile.extend()`, `FitFile.remove()`, `FitFile.pop()`
- Plugin system: register custom `Message` and `FitFile` subclasses via `fit.messages` / `fit.files` entry-point groups

### Bug fixes

- Fix `Dynamic.__init__` not propagating `base.size` — caused `struct.error` on write/read of any message containing a `Dynamic` field (e.g. `FileId.product`)
- Fix `FileId.create()` writing `product` as a raw string instead of going through the `garmin_product` subfield — caused `struct.error` on write
- Fix `KNOWN` type registry: filter out `@property` descriptors (`Dynamic.type`) via `isinstance(val, int)`
- Fix `Type.__hash__` missing after defining `__eq__`
- Fix integer division in `ArrayType`: `/` → `//`
- Fix `".FIT"` literal → `b".FIT"` (struct unpacks `4s` as bytes in Python 3)
- Fix `0xDEADBEAF` typo → `0xDEADBEEF` in `FileId`
- Fix bytes handling: `ord(chunk[i])` → `chunk[i]`, `"".join()` → `b"".join()`

### Refactoring

- Replace `Meta(dict)` with a proper `@dataclass` — typed, introspectable, no dict-access magic
- Move all business logic out of `__init__.py` files into dedicated modules (`fitfile.py`, `messages/message.py`, `types/base.py`, `files/filelike.py`, `record/constants.py`); `__init__.py` files are now thin re-export stubs
- Replace `setup.py` with `pyproject.toml`
- Add `py.typed` marker (PEP 561)
- Add full type annotations, `from __future__ import annotations`, and docstrings throughout

### Infrastructure

- Add `pytest` test suite (122 tests, 93 % coverage)
- Add `black`, `ruff`, and `mypy` configuration
- Add `pre-commit` configuration
- Add Makefile for common development tasks
- Add `tox.ini` for multi-version testing (py39, py310, py312)
- Add GitHub Actions CI matrix (Python 3.9, 3.10, 3.12, 3.13)

## 0.4.1 (2014-xx-xx)

- Last Python 2 release
