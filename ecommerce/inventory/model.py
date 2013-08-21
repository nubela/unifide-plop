from base.base_model import Base


class Inventory(Base):
    def __init__(self, **kwargs):
        super(Inventory, self).__init__()

        self.container_id = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    @staticmethod
    def unserialize(dic):
        return Inventory(**dic)

    @staticmethod
    def coll_name():
        return "inventories"