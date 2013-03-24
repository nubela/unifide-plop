from base.scheduling import SchedulingBase

def schedulable(save_fn):
    def save_schedule_info(obj):
        id = save_fn(obj)
        coll = SchedulingBase.collection()
        coll.insert(obj.schedule_serialize(id))
        return id

    return save_schedule_info