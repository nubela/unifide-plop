from base.base_model import Base


class Comment(Base):
    def __init__(self, **kwargs):
        super(Comment, self).__init__()

        self.user_id = None
        self.comment = None
        self.obj_id = None
        self.coll_name = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    @property
    def user(self):
        from base import users
        return users.get(self.user_id)

    @staticmethod
    def unserialize(dic):
        return Comment(**dic)

    @staticmethod
    def coll_name():
        return "comment"