class FormatError(Exception):
    pass


class HeaderFormatError(FormatError):
    pass


class BodyFormatError(FormatError):
    pass


class CrcFormatError(FormatError):
    pass
