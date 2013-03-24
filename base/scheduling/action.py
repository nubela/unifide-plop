from base.scheduling.model import SchedulingBase
import pymongo

def get_before(obj_type, dt_obj, limit=1):
    collection = SchedulingBase.collection()
    results = collection.find({"publish_datetime": {"$lt": dt_obj}}, limit=limit).sort("publish_datetime",
        pymongo.DESCENDING)
    objs = [obj_type.unserialize(x) for x in results]
    return objs


def get_after(obj_type, dt_obj, limit=1):
    collection = SchedulingBase.collection()
    results = collection.find({"publish_datetime": {"$gt": dt_obj}}, limit=limit).sort("publish_datetime")
    objs = [obj_type.unserialize(x) for x in results]
    return objs
