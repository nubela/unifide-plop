from base.base_model import Base


class Discount(Base):
    """
    Describe the rules that govern how discounts will work in an eCommerce enabled store
    """
    def __init__(self, **kwargs):
        super(Discount, self).__init__()

        #applied on (scope)
        self.collection_name = None
        self.obj_id = None
        self.discount_scope = None

        #discount attr
        self.discount_percentage = 0 # 0-100
        self.absolute_discounted_price = 0 # discount in absolute digits

        #rule attr
        self.item_minimum_spending = None # minimum spending
        self.order_minimum_spending = None # minimum spending
        self.begins_utc_datetime = None # utc datetime_obj
        self.expire_utc_datetime = None # utc datetime_obj
        self.discount_lifetime_type = None

        #status
        self.name = None
        self.description = None
        self.status = None
        self.admin_id = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    @staticmethod
    def unserialize(dic):
        return Discount(**dic)

    @staticmethod
    def coll_name():
        return "discounts"