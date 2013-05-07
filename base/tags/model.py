from base.base_model import Base


class Tag(Base):
    def __init__(self, **kwargs):
        super(Tag, self).__init__()

        self.tag = None
        self.obj_id = None
        self.coll_name = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    @staticmethod
    def unserialize(dic):
        return Tag(**dic)

    @staticmethod
    def coll_name():
        return "tag"