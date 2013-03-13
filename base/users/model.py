class User:
    def __init__(self):
        self.id = None
        self.username = None
        self.first_name = ""
        self.middle_name = ""
        self.last_name = ""
        self.email = None

        #facebook oauth
        self.fb_id = None
        self.gender = None
        self.username = None
        self.link = None


    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def is_anon(self):
        return self.username is None and self.first_name is "" or self.email is None

    @staticmethod
    def unserialize(self, json):
        return User(**json.loads(json))