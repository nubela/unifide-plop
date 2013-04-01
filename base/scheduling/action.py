import datetime
import pymongo

def sort_asc(obj_lis):
    return sorted(obj_lis, key=lambda x: x.publish_datetime)


def sort_desc(obj_lis):
    return reversed(sort_asc(obj_lis))


def filter_before(obj_lis, before_dt=None):
    """
    Filter a list of objects with SchedulingBase that meets the datetime cut off date
    as provided by `before_dt`
    """
    if before_dt is None:
        before_dt = datetime.datetime.utcnow()
    return filter(lambda x: x.publish_datetime <= before_dt, obj_lis)


def filter_after(obj_lis, after_dt=None):
    """
    Filter a list of objects with SchedulingBase that meets the datetime cut off date
    as provided by `before_dt`
    """
    if after_dt is None:
        after_dt = datetime.datetime.utcnow()
    return filter(lambda x: x.publish_datetime >= after_dt, obj_lis)


def get_before(obj_type, before_dt=None, limit=1, sort_args=None, find_param_lis=None):
    """
    Get objects that were scheduled to be published up till the given datetime object.

    - `sorg_args` is a list that is applied to the .sort() method in the pymongo's find() chain.
      It is defaulted to sorting the scheduled datetime on a descending order.

    - `find_param_kwargs` is the parameter for custom search params in find()
    """
    if before_dt is None:
        before_dt = datetime.datetime.utcnow()
    if find_param_lis is None:
        find_param_lis = []
    if sort_args is None:
        sort_args = ("publish_datetime", pymongo.DESCENDING)

    collection = obj_type.collection()
    find_dic = {
        "$and": [
                    {"publish_datetime": {"$lt": before_dt}}
                ] + find_param_lis,
    }
    results = collection.find(find_dic, limit=limit).sort(*sort_args)
    objs = [obj_type.unserialize(x) for x in results]
    return objs


def get_after(obj_type, after_dt=None, limit=1, sort_args=None, find_param_lis=None):
    """
    Get objects that were scheduled to be published up till the given datetime object.

    - `sorg_args` is a list that is applied to the .sort() method in the pymongo's find() chain.
      It is defaulted to sorting the scheduled datetime on a descending order.

    - `find_param_kwargs` is the parameter for custom search params in find()
    """
    if after_dt is None:
        after_dt = datetime.datetime.utcnow()
    if find_param_lis is None:
        find_param_lis = []
    if sort_args is None:
        sort_args = ("publish_datetime", pymongo.ASCENDING)

    collection = obj_type.collection()
    find_dic = {
        "$and": [
                    {"publish_datetime": {"$gt": after_dt}}
                ] + find_param_lis,
    }

    results = collection.find(find_dic, limit=limit).sort(*sort_args)
    objs = [obj_type.unserialize(x) for x in results]
    return objs