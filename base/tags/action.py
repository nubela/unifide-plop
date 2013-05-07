from base.tags.model import Tag


def save(tag_obj):
    return Tag.collection().save(tag_obj.serialize())


def tag(obj, tag_name):
    #check for dupes
    all_tags = get_tags(obj)
    conflict_filtered = filter(lambda x: x.tag == tag_name, all_tags)
    if len(conflict_filtered) > 0:
        return conflict_filtered[0]

    tag_obj = Tag()
    tag_obj.obj_id = obj.obj_id()
    tag_obj.coll_name = obj.__class__.coll_name()
    tag_obj.tag = tag_name
    tag_obj._id = save(tag_obj)
    return tag_obj


def get_tags(obj):
    id = obj.obj_id()
    coll_name = obj.__class__.coll_name()
    lis = Tag.collection().find({
        "coll_name": coll_name,
        "obj_id": id,
    })
    return [Tag.unserialize(dic) for dic in lis]


def clear(obj):
    id = obj.obj_id()
    coll_name = obj.__class__.coll_name()
    Tag.collection().remove({
        "coll_name": coll_name,
        "obj_id": id,
    })