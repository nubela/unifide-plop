from base import users
from base.base_model import Base


class Order(Base):
    def __init__(self, **kwargs):
        super(Order, self).__init__()

        self.user_id = None
        self.obj_id = None
        self.coll_name = None
        self.quantity = None
        self.special_notes = None

        self.status = None
        self.status_private_notes = None
        self.status_public_notes = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def serialize(self, json_friendly=False):
        dic = super(Order, self).serialize(json_friendly)
        if json_friendly:
            user_obj = users.get(self.user_id)
            dic["user"] = user_obj.serialize(json_friendly)
            obj_obj = COLLECTION_MAP[self.coll_name]["get"](self.obj_id)
            dic["object"] = obj_obj.serialize(json_friendly)
        return dic

    @staticmethod
    def unserialize(dic):
        return Order(**dic)

    @staticmethod
    def coll_name():
        return "order"