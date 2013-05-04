import datetime
from bson import ObjectId


class OrgInfo():
    #enumerator
    ADDRESS = "address"
    ORG_NAME = "name"
    CONTACT_EMAIL = "email"
    BIZ_DESCRIPTION = "description"

    def __init__(self, **kwargs):
        self.name = None
        self.address = None
        self.email = None
        self.description = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def serialize(self, json_friendly=False):
        dic = {k: v for k, v in self.__dict__.iteritems()}

        if json_friendly:
            for k, v in dic.items():
                if type(v) == datetime.datetime:
                    dic[k] = datetime.time.mktime(v.timetuple())
                elif type(v) == ObjectId:
                    dic[k] = str(v)
        return dic