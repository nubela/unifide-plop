import datetime
import pymongo

def get_before(obj_type, before_dt=None, limit=1, sort_args=None, find_param_kwargs=None):
    """
    Get objects that were scheduled to be published up till the given datetime object.

    - `sorg_args` is a list that is applied to the .sort() method in the pymongo's find() chain.
      It is defaulted to sorting the scheduled datetime on a descending order.

    - `find_param_kwargs` is the parameter for custom search params in find()
    """
    if before_dt is None:
        before_dt = datetime.datetime.utcnow()
    if find_param_kwargs is None:
        find_param_kwargs = {}
    if sort_args is None:
        sort_args = ("publish_datetime", pymongo.DESCENDING)

    collection = obj_type.collection()
    find_dic = {
        "$and": [{k: v} for k, v in find_param_kwargs.iteritems()] + [{"publish_datetime": {"$lt": before_dt}}],
    }
    results = collection.find(find_dic, limit=limit).sort(*sort_args)
    objs = [obj_type.unserialize(x) for x in results]
    return objs


def get_after(obj_type, after_dt=None, limit=1, sort_args=None, find_param_kwargs=None):
    """
    Get objects that were scheduled to be published up till the given datetime object.

    - `sorg_args` is a list that is applied to the .sort() method in the pymongo's find() chain.
      It is defaulted to sorting the scheduled datetime on a descending order.

    - `find_param_kwargs` is the parameter for custom search params in find()
    """
    if after_dt is None:
        after_dt = datetime.datetime.utcnow()
    if find_param_kwargs is None:
        find_param_kwargs = {}
    if sort_args is None:
        sort_args = ("publish_datetime", pymongo.ASCENDING)

    collection = obj_type.collection()
    find_dic = {
        "$and": [{k: v} for k, v in find_param_kwargs.iteritems()] + [{"publish_datetime": {"$lt": after_dt}}],
    }
    results = collection.find(find_dic, limit=limit).sort(*sort_args)
    objs = [obj_type.unserialize(x) for x in results]
    return objs