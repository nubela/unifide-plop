from functools import wraps
import uuid
from datetime import datetime
import time
from random import choice
import os

from flask import request, current_app
from bson import ObjectId

from cfg import ASSETS_FOLDER


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


def __gen_random_datetime(random_day_range, __cache__={}):
    seconds_a_day = 24 * 60 * 60
    now = datetime.utcnow()
    timestamp = __serialize_json_datetime(now)
    start_timestamp = timestamp - (random_day_range * seconds_a_day)
    end_timestamp = timestamp + (random_day_range * seconds_a_day)

    cache_key = "%d%d" % (int(start_timestamp), int(end_timestamp))
    if cache_key not in __cache__:
        __cache__[cache_key] = range(int(start_timestamp), int(end_timestamp))

    random_timestamp = choice(__cache__[cache_key])
    return __unserialize_json_datetime(random_timestamp)


def jsonp(func):
    """Wraps JSONified output for JSONP requests."""

    @wraps(func)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            data = str(func(*args, **kwargs).data)
            content = str(callback) + '(' + data + ')'
            mimetype = 'application/javascript'
            return current_app.response_class(content, mimetype=mimetype)
        else:
            return func(*args, **kwargs)

    return decorated_function