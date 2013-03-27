import uuid
from datetime import datetime
import time
from cfg import ASSETS_FOLDER
import os
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


def read_template(relative_template_path, templates_folder=None):
    if templates_folder is None:
        templates_folder = os.path.join(ASSETS_FOLDER, "html")
    file_path = os.path.join(templates_folder, relative_template_path)
    f = open(file_path, 'r')
    return f.read()
