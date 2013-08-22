import uuid
from base.base_model import Base
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

    @property
    def sluggify(self):
        from base import slugs


        return slugs.sluggify(self.name, self._id, Container.coll_name())


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
        self.custom_attr_lis = []
        self.custom_media_lis = []

        #meta
        self.group_id = str(uuid.uuid1())
        self.container_id = None
        self.status = ItemStatus.VISIBLE

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    @property
    def sluggify(self):
        from base import slugs


        return slugs.sluggify(self.name, self._id, Item.coll_name())

    @property
    def tags(self):
        from base import tags


        return [x.tag for x in tags.get_tags(self)]

    @property
    def media_url(self):
        from base import media


        if self.media_id is not None:
            return media.url_for(media.get(self.media_id))
        return None


    def serialize(self, json_friendly=False):
        from base import media, tags


        dic = super(Item, self).serialize(json_friendly)
        if json_friendly:
            dic["tags"] = [x.tag for x in tags.get_tags(self)]
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