from base.base_model import Base
from base.scheduling import SchedulingBase

class StockAvailability(SchedulingBase):
    def __init__(self, **kwargs):
        super(StockAvailability, self).__init__()

        self.obj_id = None
        self.coll_name = None
        self.availability = None #integer, float

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    @staticmethod
    def unserialize(dic):
        return StockAvailability(**dic)

    @staticmethod
    def coll_name():
        return "stock_avail"


class Order(Base):
    def __init__(self, **kwargs):
        super(Order, self).__init__()

        self.user_id = None
        self.obj_id = None
        self.coll_name = None

        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    @staticmethod
    def unserialize(dic):
        return Order(**dic)

    @staticmethod
    def coll_name():
        return "orders"