from base.tags.model import Tag


def save(tag_obj):
    return Tag.collection().save(tag_obj.serialize())


def get_all(obj_cls, tag_name):
    """
    Gets a list of objects from a object class that is tagged with the provided tag_name

    :return list of objects:
    """
    all_tag_objs = Tag.collection().find({
        "coll_name": obj_cls.coll_name(),
        "tag": tag_name,
    })

    all_obj_ids = map(lambda x: x["obj_id"], all_tag_objs)
    all_objs = obj_cls.collection().find({
        "_id": {
            "$in": [all_obj_ids]
        }
    })
    return map(lambda x: obj_cls.unserialize(x), all_objs)


def tag(obj, tag_name):
    """
    Tag an object with a tag name
    :param obj:
    :param tag_name:
    :return:
    """
    #check for dupes
    all_tags = get_tags(obj)
    conflict_filtered = filter(lambda x: x.tag == tag_name, all_tags)
    if len(conflict_filtered) > 0:
        return conflict_filtered[0]

    tag_obj = Tag()
    tag_obj.obj_id = obj._id
    tag_obj.coll_name = obj.__class__.coll_name()
    tag_obj.tag = tag_name
    tag_obj._id = save(tag_obj)
    return tag_obj


def get_tags(obj):
    """
    Get all tags that an object is tagged with

    :param obj:
    :return list of tags:
    """
    id = obj._id
    coll_name = obj.__class__.coll_name()
    lis = Tag.collection().find({
        "coll_name": coll_name,
        "obj_id": id,
    })
    return [Tag.unserialize(dic) for dic in lis]


def clear(obj):
    """
    Clear an object of tags

    :param obj:
    :return:
    """
    id = obj._id
    coll_name = obj.__class__.coll_name()
    Tag.collection().remove({
        "coll_name": coll_name,
        "obj_id": id,
    })