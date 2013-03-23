#general
SECRET_KEY = "b4ef3a73-5d52-11e2-9b58-14109feb3038"
DOMAIN = "http://localhost:5001"
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