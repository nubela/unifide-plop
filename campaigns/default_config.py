#default config (do not edit these)
import os

here = os.path.dirname(os.path.realpath(__file__))
CAMPAIGNS_ASSET_DIR = os.path.join(here, "_assets")
MOCK_DATE_RANGE_DAYS = 100

#always try to use base config if they exist
try:
    from local_config import *
except ImportError:
    pass