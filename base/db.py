from cfg import MONGO_HOST, MONGO_PORT, MONGO_DB
from pymongo import MongoClient

def get_mongo(db=[]):
    """
    This function employs a good ol` gotcha with using mutable objects as a default value for an argument to cache
    the database object.

    If the `db` arg is an empty list, populate it with the object.
    Every other call to this function will skip the if clause and return the cached `db` object.
    Win.
    """
    if db == []:
        connection = MongoClient(MONGO_HOST, MONGO_PORT)
        mongo_db = connection[MONGO_DB]
        db += [mongo_db]
    return db[0]