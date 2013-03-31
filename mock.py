# create mock data for the various reusable packages
import importlib
from cfg import INSTALLED_PACKAGES, MONGO_HOST, MONGO_PORT, MONGO_DB
from pymongo import MongoClient

if __name__ == "__main__":
    #reset db
    print "Dropping existing database.."
    connection = MongoClient(MONGO_HOST, MONGO_PORT)
    connection.drop_database(MONGO_DB)

    for package in INSTALLED_PACKAGES:
        #try to import mocking util
        try:
            pkg = __import__("%s.mock" % package)
            pkg = importlib.import_module("%s.mock" % package)
            pkg.mock_and_save()
        except ImportError:
            print "Nothing to mock for \"%s\"" % (package)