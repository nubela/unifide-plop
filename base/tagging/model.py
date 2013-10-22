from base.base_model import Base

class Tag(Base):
    def __init__(self):
        super(Tag, self).__init__()

        name = None
        description = None

        for k, v in Tag.iteritems():
            setattr(self, k, v)

    @staticmethod
    def unserialize(dic):
        return Tag(**dic)

    @staticmethod
    def coll_name():
        return "tags"


class TagLog(Base):
    def __init__(self):
        super(TagLog, self).__init__()

        tag_id = None
        obj_class_name = None
        object_id_lis = []

        for k, v in TagLog.iteritems():
            setattr(self, k, v)

    @staticmethod
    def unserialize(dic):
        return TagLog(**dic)

    @staticmethod
    def coll_name():
        return "tag_logs"