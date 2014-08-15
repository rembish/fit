from importlib import import_module
from inspect import getmembers, isclass
from pkgutil import iter_modules


class FileMixin(object):
    file_type = None


def get_known():
    main = import_module(__name__)
    known = {}

    for _, module_name, _ in iter_modules(main.__path__, "%s." % __name__):
        module = import_module(module_name)
        for _, obj in getmembers(module, isclass):
            if issubclass(obj, FileMixin):
                known[obj.file_type] = obj

    return known


KNOWN = get_known()
del get_known
