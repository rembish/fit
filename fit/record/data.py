from fit.record import Record


class Data(Record):
    @classmethod
    def read(cls, owner, header, buffer):
        definition = owner.definitions[header.type]
        record = definition.build_message(buffer)
        owner.append(record)

        return record
