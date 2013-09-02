from base.base_model import Base


class TaxRule(Base):
    def __init__(self, **kwargs):
        super(TaxRule, self).__init__()

        self.name = None
        self.description = None
        self.tax_perc = 0
        self.status = None
        self.admin_id = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    @staticmethod
    def unserialize(dic):
        return TaxRule(**dic)

    @staticmethod
    def coll_name():
        return "tax_rules"