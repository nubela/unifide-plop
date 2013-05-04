from base.base_model import Base
from base import media
from base.scheduling.model import SchedulingBase


class Container(Base):
    """
    Equivalent to a folder. Contain items.
    """

    def __init__(self, **kwargs):
        super(Container, self).__init__()

        self.name = None
        self.description = None
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
        return "container"


class Item(SchedulingBase):
    def __init__(self, **kwargs):
        super(Item, self).__init__()

        #basic attr
        self.name = None
        self.media_id = None
        self.description = None
        self.quantity = None
        self.price = None

        #meta
        self.container_id = None
        self.status = ItemStatus.VISIBLE

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def serialize(self, json_friendly=False):
        dic = super(Item, self).serialize(json_friendly)

        if self.media_id is not None:
            dic["media_url"] = media.url_for(media.get(self.media_id))
        else:
            dic["media_url"] = None

        return dic

    @staticmethod
    def unserialize(dic):
        return Item(**dic)

    @staticmethod
    def coll_name():
        return "item"


class ItemStatus:
    HIDDEN = "hidden"
    VISIBLE = "visible"