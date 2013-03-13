class Base:
    def save(self):
        """
        Saves this object in the mongo database

        :return:
        """
        pass

    def serialize(self):
        return {k:v for k,v in  self.__dict__.iteritems()}

    @staticmethod
    def unserialize(self, json):
        pass