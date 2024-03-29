import datetime
import time
from pprint import pprint
from bson import ObjectId
from base.db import get_mongo
from base.util import coerce_bson_id


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
        return self._id

    def serialize(self, json_friendly=False):
        dic = {k: v for k, v in self.__dict__.iteritems()}

        if json_friendly:
            for k, v in dic.items():
                if type(v) == datetime.datetime:
                    dic[k] = time.mktime(v.timetuple())
                elif type(v) == ObjectId:
                    dic[k] = str(v)
        return dic

    def save(self):
        self.modification_timestamp_utc = datetime.datetime.utcnow()
        col = self.collection()
        id = col.save(self.serialize(), safe=True)
        return id

    @staticmethod
    def unserialize(json):
        pass

    @classmethod
    def collection(cls, coll={}):
        if cls.coll_name() not in coll:
            mongo_db = get_mongo()
            collection = mongo_db[cls.coll_name()]
            coll[cls.coll_name()] = collection
        return coll[cls.coll_name()]

    @staticmethod
    def coll_name():
        return ""