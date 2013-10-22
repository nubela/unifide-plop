from base.tagging.model import Tag, TagLog

def save(tag_obj):
    coll = Tag.collection()
    id = coll.save(tag_obj.serialize())
    return id


def save_tag(tag_name, description=None):
    tag_obj = Tag()
    tag_obj.name = tag_name
    tag_obj.description = description
    tag_obj._id = save(tag_obj)
    return tag_obj


def get_tag(tag_name):
    coll = Tag.collection()
    dic = coll.find_one({"name": tag_name})
    return Tag.unserialize(dic) if dic is not None else None


def save_tag_log(tag_log_obj):
    coll = TagLog.collection()
    id = coll.save(tag_log_obj.serialize())
    return id


def save_tag_log_attr(tag, obj_class):
    tag_log_obj = TagLog()
    tag_log_obj.tag_id = tag.obj_id()
    tag_log_obj.obj_class_name = obj_class.__name__
    tag_log_obj._id = save_tag_log(tag_log_obj)
    return tag_log_obj


def get_tag_log(tag, obj_class):
    coll = TagLog.collection()
    dic = coll.find_one({
        "tag_id": tag.obj_id(),
        "obj_class_name": obj_class.__name__,
    })
    return TagLog.unserialize(dic) if dic is not None else None


def tag(obj, tag):
    #get log to save into
    tag_log = get_tag_log(tag, obj.__class__)
    if tag_log is None: tag_log = save_tag_log_attr(tag, obj.__class__)

    #save in log
    tag_log.object_id_lis += [obj.obj_id()]
    save_tag_log(tag_log)

    #save in obj
    if not hasattr(obj, "tags"):
        obj.tags = []
    obj.tags += [tag.name]
    obj_coll = obj.collection()
    obj_coll.save(obj)


def get_tagged_ids(object_class, tag):
    """
    Get objects ids that belong to a certain class that are tagged with the given `Tag` object
    """
    tag_log = get_tag_log(tag, object_class)
    if tag_log is not None:
        return tag_log.object_id_lis
    return []