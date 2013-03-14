from campaigns import save
from campaigns.campaign.mock_util import gen_campaigns

def mock_and_save():
    print "Mocking campaigns.."
    campaigns = gen_campaigns()
    for c in campaigns:
        save(c)
    print "Done mocking campaigns"