from base.db import get_mongo
from base.scheduling.decorator import schedulable
from campaigns.default_config import MONGO_COLLECTION_NAME


def get(campaign_obj_id):
    """
    Gets a campaign with the given id

    :param campaign_obj_id:
    :return:
    """
    collection = __get_collection()
    if campaign_obj_id is None:
        return collection.find_one()
    return collection.find_one({"_id": campaign_obj_id})


@schedulable
def save(campaign_obj):
    col = __get_collection()
    id = col.insert(campaign_obj.serialize())
    return id


def __get_collection(coll=[]):
    if coll == []:
        mongo_db = get_mongo()
        collection = mongo_db[MONGO_COLLECTION_NAME]
        coll += [collection]
    return coll[0]