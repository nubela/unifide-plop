import datetime
from base.db import get_mongo
from bson.objectid import ObjectId

class Base(object):
    def __init__(self):
        self.timestamp_utc = datetime.datetime.utcnow()
        self.modification_timestamp_utc = datetime.datetime.utcnow()

    def id(self):
        return str(self._id)

    def obj_id(self):
        """
        for pymongo parsing
        """
        return ObjectId(str(self._id))

    def serialize(self):
        banned_keys = ["_id", ]
        return {k: v for k, v in self.__dict__.iteritems() if k not in banned_keys}

    @staticmethod
    def unserialize(json):
        pass

    @classmethod
    def collection(cls, coll=[]):
        if coll == []:
            mongo_db = get_mongo()
            collection = mongo_db[cls.coll_name()]
            coll += [collection]
        return coll[0]

    @staticmethod
    def coll_name():
        return ""