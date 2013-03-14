from base.base_model import Base

class SchedulingBase(Base):
    def __init__(self):
        self.publish_datetime = None

    def schedule_serialize(self, obj_id):
        dic = {
            "obj_id": obj_id,
            "publish_datetime": self.publish_datetime,
            }
        return dic