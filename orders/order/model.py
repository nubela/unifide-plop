from base.base_model import Base


class Order(Base):
    def __init__(self, **kwargs):
        super(Order, self).__init__()

        self.user_id = None
        self.status = None
        self.items = [] # {obj_id: None, quantity:None}
        self.request_notes = None
        self.admin_notes = None
        self.admin_id = None

        #extra stuff like taxes, shipping, discounts, etc
        self.debits = [] # {obj_id: None, coll_name: None, amount=None}
        self.credits = [] # {obj_id: None, coll_name: None, amount=None}

        #convenience attr
        self.nett_total = 0

        for k, v in kwargs.iteritems():
            setattr(self, k, v)


    @property
    def total_price(self):
        import orders


        return orders.total_price(self)

    @property
    def nett_price(self):
        import orders


        return orders.nett_price(self)

    def serialize(self, json_friendly=False):
        dic = super(Order, self).serialize(json_friendly)
        return dic

    @staticmethod
    def unserialize(dic):
        return Order(**dic)

    @staticmethod
    def coll_name():
        return "orders"