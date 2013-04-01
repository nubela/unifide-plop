from base.base_model import Base
from base.scheduling.model import SchedulingBase


class Container(Base):
    """
    Equivalent to a folder. Contain items.
    """

    def __init__(self, **kwargs):
        super(Container, self).__init__()

        self.name = None
        self.slug_name = None
        self.materialized_path = None #represented in list repr
        self.parent_id = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    @staticmethod
    def unserialize(dic):
        return Container(**dic)

    @staticmethod
    def coll_name():
        return "containers"


class Item(SchedulingBase):
    INCLUDED_FIELDS = ["name", "image", "description", "price"]
    META_FIELDS = ["slug_name", "container_id", "status", "custom_attr_lis"]

    def __init__(self, **kwargs):
        super(Item, self).__init__()

        #basic attr
        self.name = None
        self.image = None
        self.description = None
        self.price = None

        #meta
        self.slug_name = None
        self.container_id = None
        self.status = None
        self.custom_attr_lis = []

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    @staticmethod
    def unserialize(dic):
        return Item(**dic)

    @staticmethod
    def coll_name():
        return "items"


class ItemStatus:
    HIDDEN = "hidden"
    VISIBLE = "visible"