from base.base_model import Base
from base.util import _gen_uuid


class User(Base):

    def __init__(self, **kwargs):
        self._id = _gen_uuid()
        self.username = None
        self.first_name = ""
        self.middle_name = ""
        self.last_name = ""
        self.email = None
        self.address = None
        self.passwd_hash = None

        #facebook oauth
        self.fb_id = None
        self.gender = None
        self.link = None

        #account meta
        self.groups = []
        self.account_status = None
        self.tokens = {}

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def is_authenticated(self):
        return True

    def is_active(self):
        from base.users import AccountStatus

        return True
        # return self.account_status == AccountStatus.ENABLED

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
        return "plop_users"


class Group(Base):
    def __init__(self, **kwargs):

        self.name = None
        self.description = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    @staticmethod
    def unserialize(dic):
        return Group(**dic)

    @staticmethod
    def coll_name():
        return "groups"