#general
from base import S3

UPLOAD_RELATIVE_ENDPOINT = "/media/uploads/"
UPLOAD_FOLDER = "/home/nubela/Workspace/unifide-plop/support/uploads"
ASSETS_FOLDER = "/home/nubela/Workspace/unifide-plop/base/assets/"
SECRET_KEY = "b4ef3a73-5d52-11e2-9b58-14109feb3038"
DOMAIN = "http://localhost:5001"
MOCK_MODE = False
INSTALLED_PACKAGES = [
    "articles",
    "campaigns",
    "ecommerce",
    "orders",
    "base.items",
    "base.org"
]

#mongodb
MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "unifide"
if MOCK_MODE:
    MONGO_DB = "mock"

#mock stuff
MOCK_DATE_RANGE_DAYS = 100

#amazon s3 / upload folder
AWS_ACCESS_KEY_ID = 'AKIAIYOWWMY2JWOT7YAA'
AWS_SECRET_ACCESS_KEY = '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'
S3_BUCKET_NAME = "ctrleff"
S3_BUCKET_CHECK = False
S3_KEY_NAME = "ctrleff"
S3_LOCATION = S3.Location.SG
CLOUDFRONT_URL = "http://d3rdt3fjkv9h3z.cloudfront.net/"

#local uploads
UPLOAD_FOLDER = "/Users/nubela/Workspace/unifide-backend/resources"
UPLOAD_METHOD = "local" #or s3
UPLOAD_RELATIVE_ENDPOINT = "resources"