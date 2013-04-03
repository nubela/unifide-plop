class OrgInfo():
    #enumerator
    ADDRESS = "address"
    ORG_NAME = "name"
    CONTACT_EMAIL = "email"
    BIZ_DESCRIPTION = "description"

    def __init__(self, **kwargs):
        self.name = None
        self.address = None
        self.email = None
        self.description = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)