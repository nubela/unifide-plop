from base.base_model import Base


class Coupon(Base):
    def __init__(self, **kwargs):
        super(Coupon, self).__init__()

        #applied on (scope)
        self.coupon_scope = None
        self.collection_name = None
        self.obj_id = None

        #discount attr
        self.coupon_code = None
        self.coupon_value = 0 # discount in absolute digits

        #rule attr
        self.valid_times = 0
        self.order_minimum_spending = None # minimum spending
        self.begins_utc_datetime = None # utc datetime_obj
        self.expire_utc_datetime = None # utc datetime_obj
        self.coupon_lifetime_type = None
        self.user_scope = None
        self.user_id = None
        self.user_group = None

        #status
        self.name = None
        self.description = None
        self.status = None
        self.admin_id = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    @staticmethod
    def unserialize(dic):
        return Coupon(**dic)

    @staticmethod
    def coll_name():
        return "coupons"

class CouponLog(Base):
    def __init__(self, **kwargs):
        super(CouponLog, self).__init__()

        self.used_date_utc = None
        self.user_id = None
        self.order_id = None
        self.discounted_total = 0

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    @staticmethod
    def unserialize(dic):
        return CouponLog(**dic)

    @staticmethod
    def coll_name():
        return "coupon_logs"