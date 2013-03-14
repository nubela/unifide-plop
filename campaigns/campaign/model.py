from base.scheduling.model import SchedulingBase


class Campaign(SchedulingBase):
    def __init__(self, **kwargs):
        self.title = None
        self.description = None
        self.picture_url = None
        self.type = None
        self.item_id_lis = []

        #event specific
        self.happening_datetime = None
        self.rsvped_users_ids = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    @staticmethod
    def unserialize(dic):
        return Campaign(**dic)


class CampaignType:
    EVENT = "event"
    PROMOTION = "promotion"
    ALL = "all"