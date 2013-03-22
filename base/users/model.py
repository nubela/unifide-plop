from base.base_model import Base


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

        for k, v in kwargs.iteritems():
            setattr(self, k, v)


    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)


    @staticmethod
    def unserialize(json):
        return User(**json.loads(json))