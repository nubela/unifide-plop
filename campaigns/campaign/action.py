from campaigns.campaign.model import CampaignType

def get(campaign_obj_id):
    """
    Gets a campaign with the given id

    :param campaign_obj_id:
    :return:
    """
    pass


def get_all(type=CampaignType.ALL, limit=5):
    """
    Get all campaigns up to _now_, capped by a stated limit.

    :param type:
    :param limit:
    :return:
    """
    pass


def get_all_in_duration(from_datetime, to_datetime):
    pass


def put_comment(campaign_obj, comment_obj):
    pass