from base.db import get_mongo
from base.users.default_config import USERS_COLLECTION_NAME
from base.users.util import __gen_passwd_hash


def send_confirmation(saved_user_obj,
                      confirmation_email_subject,
                      confirmation_email_html):
    pass


def get_user_by_attr(attr_dic):
    coll = __get_collection()
    return coll.find_one(attr_dic)


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
    coll.update({'_id': saved_user_obj._id}, {"$set": saved_user_obj.serialize()}, upsert=False)
    return saved_user_obj


def generate_token(user_obj, account_activity):
    """
    Generates a lasting token for a specific account activity.
    (EG: Email verification of a new account)

    Removes an existing if it already exists, and then replace
    it with a new one that this will generate.
    """
    pass


def remove_token(user_obj, account_activity):
    """
    Removes a token for a specific account activity.
    (EG: When a user has a verified his/her new account)

    Does nothing if there does not exists a token for
    the activity.
    """
    pass


def __get_token(user_obj, account_activity):
    """
    Fetches token for a user's account activity.
    Returns None if it does not exists.
    """
    pass


def check_token(user_obj, account_activity, token):
    """
    Returns a boolean on whether a token is the correct
    token for a specific account activity for a user.
    """
    pass


class AccountActivity:
    VERIFY_EMAIL_ADDR = "verify_email"
    RESET_PASSWORD = "passwd_reset"


class AccountStatus:
    ENABLED = "enabled"
    AWAITING_CONFIRMATION = "awaiting_confirmation"
    DISABLED = "disabled"