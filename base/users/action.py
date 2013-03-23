from base import emails
from base.db import get_mongo
from base.users.model import User
from base.users.default_config import USERS_COLLECTION_NAME
from base.users.util import gen_passwd_hash
from base.util import __gen_uuid
from bson.objectid import ObjectId
from cfg import DOMAIN
from support.app import login_manager
from support.util.template import read_template


def get(user_id):
    coll = __get_collection()
    dic = coll.find_one({"_id": ObjectId(str(user_id))})
    user_obj = User.unserialize(dic)
    return user_obj


def confirm(user_obj):
    """
    Updates a newly registered user account from a AWAITING_CONFIRMATION status
    to an ENABLED status.

    :param user_obj:
    :return:
    """
    coll = __get_collection()
    user_obj.account_status = AccountStatus.ENABLED
    coll.update({'_id': ObjectId(user_obj._id)}, {"$set": user_obj.serialize()}, upsert=False)


def send_confirmation(user_obj, email_subject=None, email_html=None, relative_url=None):
    if email_subject is None:
        email_subject = "Complete your account registration"
    if email_html is None:
        email_html = read_template("emails/verify_email.html")
    if relative_url is None:
        relative_url = "/register/confirm/"

    token = generate_token(user_obj, AccountActivity.VERIFY_EMAIL_ADDR)
    url = "%s%s%s/%s/" % (DOMAIN, relative_url, user_obj._id, token)
    email_html = email_html % {"url": url}
    emails.send_email(user_obj.email, email_subject, email_html, async=False)


def get_user_by_attr(attr_dic):
    coll = __get_collection()
    dic = coll.find_one(attr_dic)
    if dic is None: return None

    #found sth
    user_obj = User.unserialize(dic)
    return user_obj


def save(user_obj,
         need_confirmation=False,
         confirmation_email_subject=None,
         confirmation_email_html=None,
         confirmation_relative_url=None,
):
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

    saved_user_obj = save_obj()
    if need_confirmation:
        send_confirmation(saved_user_obj,
            confirmation_email_subject,
            confirmation_email_html,
            relative_url=confirmation_relative_url
        )

    return saved_user_obj


def is_anon(user_obj):
    return user_obj.username is None and user_obj.first_name is "" or user_obj.email is None


def __get_collection(coll=[]):
    if coll == []:
        mongo_db = get_mongo()
        collection = mongo_db[USERS_COLLECTION_NAME]
        coll += [collection]
    return coll[0]


def send_reset_passwd_notice(user_obj, email_subj, email_html):
    token = generate_token(user_obj, AccountActivity.RESET_PASSWORD)
    url = "%s/user/reset-password/%s/%s/" % (DOMAIN, user_obj.id, token)
    email_html = email_html % {"url": url}
    emails.send_email(user_obj.email, email_subj, email_html)


def set_passwd(saved_user_obj, new_passwd):
    """
    Sets a new password for a given user object that already exists in the collection
    """
    passwd_hash = gen_passwd_hash(new_passwd, saved_user_obj.id())
    saved_user_obj.passwd_hash = passwd_hash
    coll = __get_collection()
    coll.update({'_id': ObjectId(saved_user_obj._id)}, {"$set": saved_user_obj.serialize()}, upsert=False)
    return saved_user_obj


def generate_token(user_obj, account_activity):
    """
    Generates a lasting token for a specific account activity.
    (EG: Email verification of a new account)

    Removes an existing if it already exists, and then replace
    it with a new one that this will generate.
    """
    user_obj.tokens[account_activity] = __gen_uuid()

    coll = __get_collection()
    coll.update({'_id': ObjectId(user_obj._id)}, {"$set": user_obj.serialize()}, upsert=False)
    return user_obj.tokens[account_activity]


def remove_token(user_obj, account_activity):
    """
    Removes a token for a specific account activity.
    (EG: When a user has a verified his/her new account)

    Does nothing if there does not exists a token for
    the activity.
    """
    if account_activity in user_obj.tokens:
        del user_obj.tokens[account_activity]
        coll = __get_collection()
        coll.update({'_id': ObjectId(user_obj._id)}, {"$set": user_obj.serialize()}, upsert=False)


def __get_token(user_obj, account_activity):
    """
    Fetches token for a user's account activity.
    Returns None if it does not exists.
    """
    return user_obj.tokens[account_activity]


def check_token(user_obj, account_activity, token):
    """
    Returns a boolean on whether a token is the correct
    token for a specific account activity for a user.
    """
    return user_obj.tokens[account_activity] == token


def auth(user_obj, given_password):
    given_pass_hash = gen_passwd_hash(given_password, user_obj.id())
    return user_obj.passwd_hash == given_pass_hash


@login_manager.user_loader
def load_user(userid):
    return get(userid)


class AccountActivity:
    VERIFY_EMAIL_ADDR = "verify_email"
    RESET_PASSWORD = "passwd_reset"


class AccountStatus:
    ENABLED = "enabled"
    AWAITING_CONFIRMATION = "awaiting_confirmation"
    DISABLED = "disabled"