# mocking tool for campaigns
import datetime
from random import choice
from base.util import   __gen_random_datetime
from campaigns.campaign.model import CampaignType, Campaign
from campaigns.default_config import MOCK_DATE_RANGE_DAYS

__author__ = 'nubela'


def gen_campaigns(campaign_type=CampaignType.ALL, total_campaigns=100):
    """
    Generate mock campaigns

    :param campaign_type:
    :param total_campaigns:
    :param with_comments:
    :return:
    """
    if campaign_type == CampaignType.ALL:
        campaign_type = [getattr(CampaignType, attr) for attr in dir(CampaignType()) if
                         not callable(attr) and not attr.startswith("__")]
        campaign_type.remove(CampaignType.ALL)
    else: campaign_type = [campaign_type]

    #build campaigns
    now = datetime.datetime.now()
    generated_campaigns = []
    for _ in range(total_campaigns):
        c = Campaign()
        c.publish_datetime = __gen_random_datetime(MOCK_DATE_RANGE_DAYS)
        c.title = "Mock Title"
        c.description = "Mock Description"
        c.type = choice(campaign_type)
        c.picture_url = "http://lorempixel.com/400/400"

        if c.type == CampaignType.EVENT:
            c.happening_datetime = __gen_random_datetime(MOCK_DATE_RANGE_DAYS)

        generated_campaigns += [c]

    return generated_campaigns