from fit.messages import Message
from fit.types.extended import DateTime, MessageIndex
from fit.types.general import UInt32


class GenericMessage(Message):
    timestamp = DateTime(253)
    message_index = MessageIndex(254)
    part_index = UInt32(250)

    def __init__(self, definition):
        super(GenericMessage, self).__init__(definition)
        self.msg_type = None
