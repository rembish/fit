"""FIT message base class, metaclass machinery, and message registry."""

from fit.messages.message import KNOWN, Message, register

__all__ = ["KNOWN", "Message", "register"]
