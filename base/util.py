import uuid
from datetime import datetime
import time
from bson import ObjectId


def coerce_bson_id(str_id):
    return ObjectId(str(str_id))

def __gen_uuid():
    return str(uuid.uuid1())


def __unserialize_json_datetime(json_str):
    return datetime.fromtimestamp(float(json_str))


def __serialize_json_datetime(datetime_obj):
    if not datetime_obj is None:
        return time.mktime(datetime_obj.timetuple())
    return None