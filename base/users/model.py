from base.base_model import Base
from base.db import get_mongo


class User(Base):
    def __init__(self, **kwargs):
        self.username = None
        self.first_name = ""
        self.middle_name = ""
        self.last_name = ""
        self.email = None
        self.passwd_hash = None

        #facebook oauth
        self.fb_id = None
        self.gender = None
        self.username = None
        self.link = None

        #account meta
        self.account_status = None
        self.tokens = {}

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def is_authenticated(self):
        return True

    def is_active(self):
        from base.users import AccountStatus
        return self.account_status == AccountStatus.ENABLED

    def is_anonymous(self):
        return self.username is None and self.email is None

    def get_id(self):
        return self.id()

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    @staticmethod
    def unserialize(dic):
        return User(**dic)

    @staticmethod
    def coll_name():
        return "user"