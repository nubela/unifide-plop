from base.base_model import Base

class SchedulingBase(Base):
    def __init__(self):
        super(SchedulingBase, self).__init__()
        self.publish_datetime_utc = None

    def schedule_serialize(self, obj_id):
        dic = {
            "obj_id": obj_id,
            "publish_datetime": self.publish_datetime,
            }
        return dic

    @staticmethod
    def coll_name():
        return "schedules"