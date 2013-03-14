class Base:
    def __init__(self):
        self.timestamp = None
        self.modification_timestamp = None

    def serialize(self):
        return {k: v for k, v in self.__dict__.iteritems()}

    @staticmethod
    def unserialize(json):
        pass