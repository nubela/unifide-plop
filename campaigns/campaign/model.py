from base.base_model import Base


__author__ = 'nubela'


class Comment():
    def __init__(self):
        self.text = None


class Campaign(Base):
    def __init__(self, **kwargs):
        self.id = None
        self.title = None
        self.description = None
        self.picture_url = None
        self.type = None
        self.publish_datetime = None
        self.comment_id_lis = []
        self.item_id_lis = []

        #event specific
        self.happening_datetime = None
        self.rsvped_users_ids = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    @staticmethod
    def unserialize(self, json):
        return Campaign(**json.loads(json))


class CampaignType:
    EVENT = "event"
    PROMOTION = "promotion"
    ALL = "all"