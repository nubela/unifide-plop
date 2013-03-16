from base.db import get_mongo
from base.users.default_config import USERS_COLLECTION_NAME
from base.users.util import __gen_passwd_hash


def send_confirmation(saved_user_obj,
                      confirmation_email_subject,
                      confirmation_email_html):
    pass


def save(user_obj,
         need_confirmation=False,
         confirmation_email_subject=None,
         confirmation_email_html=None):
    """
    Saves and registers this user object into the database.

    if `needs_confirmation`, it will send an email to the user with the given
    email template.
    """

    def save_obj():
        coll = __get_collection()
        user_obj._id = coll.insert(user_obj.serialize())
        return user_obj

    if need_confirmation:
        assert user_obj.email is not None
        assert confirmation_email_html is not None
        assert confirmation_email_subject is not None

    saved_user_obj = save_obj()
    if need_confirmation: send_confirmation(saved_user_obj,
                                            confirmation_email_subject,
                                            confirmation_email_html)
    return saved_user_obj


def is_anon(user_obj):
    return user_obj.username is None and user_obj.first_name is "" or user_obj.email is None


def __get_collection(coll=[]):
    if coll == []:
        mongo_db = get_mongo()
        collection = mongo_db[USERS_COLLECTION_NAME]
        coll += [collection]
    return coll[0]


def send_reset_passwd_notice(user_obj, confirmation_email_html=None):
    pass


def set_passwd(saved_user_obj, new_passwd):
    """
    Sets a new password for a given user object that already exists in the collection
    """
    passwd_hash = __gen_passwd_hash(new_passwd, saved_user_obj._id)
    saved_user_obj.passwd_hash = passwd_hash
    coll = __get_collection()
    coll.update({'_id':saved_user_obj._id}, {"$set": saved_user_obj.serialize()}, upsert=False)
    return saved_user_obj


class AccountStatus:
    ENABLED = "enabled"
    AWAITING_CONFIRMATION = "awaiting_confirmation"
    DISABLED = "disabled"