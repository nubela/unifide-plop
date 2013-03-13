#default config (do not edit these)
import os

here = os.path.realpath(__file__)
CAMPAIGNS_ASSET_DIR = os.path.join(here, "_assets")

#mock variables
MOCK_DATE_RANGE_DAYS = 100

#always try to use base config if they exist
try:
    from base.local_config import *
except ImportError:
    pass