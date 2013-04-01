#default config (do not edit these)
from exceptions import ImportError

MOCK_DATE_RANGE_DAYS = 100

#always try to use base config if they exist
try:
    from cfg import *
except ImportError:
    pass
