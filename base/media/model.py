from base.base_model import Base


class Media(Base):
    def __init__(self, **kwargs):
        super(Media, self).__init__()

        self.file_name = None
        self.storage = None
        self.file_type = None
        self.url = None

        #image meta
        self.width = None
        self.height = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    @staticmethod
    def unserialize(dic):
        return Media(**dic)

    @staticmethod
    def coll_name():
        return "media"