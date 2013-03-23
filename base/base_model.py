class Base:
    def __init__(self):
        self.timestamp = None
        self.modification_timestamp = None

    def id(self):
        return str(self._id)

    def serialize(self):
        banned_keys = ["_id",]
        return {k: v for k, v in self.__dict__.iteritems() if k not in banned_keys}

    @staticmethod
    def unserialize(json):
        pass