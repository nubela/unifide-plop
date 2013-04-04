from base.base_model import Base

class Image(Base):
    def __init__(self, **kwargs):
        super(Image, self).__init__()

        self.file_name = None
        self.url = None
        self.storage = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)


    @staticmethod
    def unserialize(dic):
        return Image(**dic)


    @staticmethod
    def coll_name():
        return "images"