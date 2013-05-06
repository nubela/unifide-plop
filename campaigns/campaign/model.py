from base.base_model import Base


class Campaign(Base):
    def __init__(self, **kwargs):
        super(Campaign, self).__init__()

        self.uid = None
        self.title = None
        self.description = None
        self.picture_url = None
        self.type = None
        self.item_id_lis = []

        #event specific
        self.happening_datetime_start = None
        self.happening_datetime_end = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    @staticmethod
    def unserialize(dic):
        return Campaign(**dic)

    @staticmethod
    def coll_name():
        return "campaigns"


class CampaignType:
    EVENT = "event"
    PROMOTION = "promotion"
    ALL = "all"