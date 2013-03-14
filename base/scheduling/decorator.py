from base.scheduling.action import __get_collection

def schedulable(save_fn):
    def save_schedule_info(obj):
        id = save_fn(obj)
        coll = __get_collection()
        coll.insert(obj.schedule_serialize(id))
        return id

    return save_schedule_info