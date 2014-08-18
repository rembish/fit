from importlib import import_module
from inspect import getmembers, isclass
from pkgutil import iter_modules


def get_known(name, base_cls, key="type"):
    main = import_module(name)
    known = {}

    for _, module_name, _ in iter_modules(main.__path__, "%s." % name):
        module = import_module(module_name)
        for _, obj in getmembers(module, isclass):
            if issubclass(obj, base_cls) \
                    and getattr(obj, key, None) is not None:
                known[getattr(obj, key)] = obj

    return known
