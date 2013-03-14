import pymongo
from base.db import get_mongo
from base.scheduling.default_config import MONGO_COLLECTION_NAME

def get_before(obj_type, dt_obj, limit=1):
    collection = __get_collection()
    results = collection.find({"publish_datetime": {"$lt": dt_obj}}, limit=limit).sort("publish_datetime",
        pymongo.DESCENDING)
    objs = [obj_type.unserialize(x) for x in results]
    return objs


def get_after(obj_type, dt_obj, limit=1):
    collection = __get_collection()
    results = collection.find({"publish_datetime": {"$gt": dt_obj}}, limit=limit).sort("publish_datetime")
    objs = [obj_type.unserialize(x) for x in results]
    return objs


def __get_collection(coll=[]):
    if coll == []:
        mongo_db = get_mongo()
        collection = mongo_db[MONGO_COLLECTION_NAME]
        coll += [collection]
    return coll[0]