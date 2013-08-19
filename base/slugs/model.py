from base.base_model import Base


class Slug(Base):
    def __init__(self, **kwargs):
        super(Slug, self).__init__()

        self.name = None
        self.coll_name = None
        self.item_id = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    @staticmethod
    def unserialize(dic):
        return Slug(**dic)

    @staticmethod
    def coll_name():
        return "slugs"