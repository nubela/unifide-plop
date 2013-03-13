__author__ = 'nubela'

class Comment():
    def __init__(self):
        self.text = None


class Campaign():
    def __init__(self, **kwargs):
        self.id = None
        self.title = None
        self.description = None
        self.picture_url = None
        self.type = None
        self.publish_datetime = None

        #event specific
        self.happening_datetime = None
        self.rsvped = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def save(self):
        pass


class CampaignType:
    EVENT = "event"
    PROMOTION = "promotion"
    ALL = "all"