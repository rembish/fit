"""Internal utility helpers for runtime class discovery."""

from __future__ import annotations

from importlib import import_module
from inspect import getmembers, isclass
from pkgutil import iter_modules
from typing import Any


def get_known(name: str, base_cls: type, key: str = "type") -> dict[Any, type[Any]]:
    """Discover and return all subclasses of *base_cls* found in sub-modules of *name*.

    Imports every sub-module of the package identified by *name*, inspects
    its members, and collects classes that are subclasses of *base_cls* and
    have a non-``None`` attribute named *key*.

    Args:
        name: Fully-qualified package name (e.g. ``"fit.types"``).
        base_cls: The base class whose subclasses should be collected.
        key: Class attribute used as the dict key (default ``"type"``).

    Returns:
        A mapping of ``{getattr(cls, key): cls}`` for all discovered classes.
    """
    main = import_module(name)
    known: dict[Any, type[Any]] = {}

    for _, module_name, _ in iter_modules(main.__path__, f"{name}."):  # type: ignore[attr-defined]
        module = import_module(module_name)
        for _, obj in getmembers(module, isclass):
            if issubclass(obj, base_cls):
                val = getattr(obj, key, None)
                # Only collect when the discriminator is a plain int — this
                # excludes abstract base classes (None) and classes whose key
                # is a @property (Dynamic.type returns a property descriptor
                # at the class level).
                if isinstance(val, int):
                    known[val] = obj

    return known
