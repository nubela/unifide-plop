#general
MOCK_MODE = True
INSTALLED_PACKAGES = [
    "articles",
    "campaigns",
    "ecommerce",
    "orders",
    ]

#mongodb
MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "unifide"
if MOCK_MODE:
    MONGO_DB = "mock"

#mock stuff
MOCK_DATE_RANGE_DAYS = 100