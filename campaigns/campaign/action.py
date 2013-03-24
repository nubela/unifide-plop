from base.scheduling.decorator import schedulable
from bson.objectid import ObjectId
from campaigns.campaign.model import Campaign


def get(campaign_obj_id):
    """
    Gets a campaign with the given id

    :param campaign_obj_id:
    :return:
    """
    collection = Campaign.collection()
    if campaign_obj_id is None:
        return collection.find_one()
    dic = collection.find_one({"_id": ObjectId(str(campaign_obj_id))})
    return Campaign.unserialize(dic) if dic is not None else None


@schedulable
def save(campaign_obj):
    col = Campaign.collection()
    id = col.insert(campaign_obj.serialize())
    return id