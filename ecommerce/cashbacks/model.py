from base.base_model import Base


class CashbackRule(Base):
    """
    Depicts the rules of cashbacks
    """

    def __init__(self, **kwargs):
        super(CashbackRule, self).__init__()

        #discount attr
        self.cashback_percentage = 0 # 0-100

        #rule attr
        self.total_minimum_spending = None # total minimum spending

        #status
        self.name = None
        self.description = None
        self.status = None
        self.admin_id = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    @staticmethod
    def unserialize(dic):
        return CashbackRule(**dic)

    @staticmethod
    def coll_name():
        return "cashbacks"


class CreditStore(Base):
    """
    Logs how much a user has stored in credit from cashbacks
    """

    def __init__(self, **kwargs):
        super(CreditStore, self).__init__()

        self.user_id = None
        self.total_credit = 0

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    @staticmethod
    def unserialize(dic):
        return CreditStore(**dic)

    @staticmethod
    def coll_name():
        return "cashback_credit_store"


class CreditLog(Base):
    """
    Logs every credit/debit of the cashback value to a user account
    """

    def __init__(self, **kwargs):
        super(CreditLog, self).__init__()

        self.user_id = None
        self.cashback_rule_id = None
        self.order_id = None
        self.credited_value = 0
        self.admin_id = None
        self.type = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    @staticmethod
    def unserialize(dic):
        return CreditLog(**dic)

    @staticmethod
    def coll_name():
        return "cashback_credit_log"