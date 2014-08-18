from fit.utils import get_known


class FileMixin(object):
    file_type = None


KNOWN = get_known(__name__, FileMixin, key="file_type")
