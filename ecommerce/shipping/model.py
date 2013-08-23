from base.base_model import Base


class ShippingRule(Base):
    def __init__(self, **kwargs):
        super(ShippingRule, self).__init__()

        self.name = None
        self.description = None

        self.price_per_unit_vol_weight = 0
        self.flat_price = 0
        self.pricing_type = None

        self.min_unit_vol_weight = 0
        self.max_unit_vol_weight = 0
        self.from_location = None
        self.to_location = None

        self.status = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    @staticmethod
    def unserialize(dic):
        return ShippingRule(**dic)

    @staticmethod
    def coll_name():
        return "shipping_rules"