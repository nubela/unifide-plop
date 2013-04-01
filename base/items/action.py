#--- item functions ---
import datetime
from base.items.model import Item, Container, ItemStatus
from base.scheduling.decorator import schedulable
from base.util import coerce_bson_id
import re
import unidecode


def get(item_id):
    """
    Get item from id
    """
    coll = Item.collection()
    dic = coll.find_one({"_id": coerce_bson_id(item_id)})
    return Item.unserialize(dic) if dic is not None else None


def item_from_path(path_lis):
    """
    Get item from path, returns None if nothing found
    """
    container_obj = container_from_path(container_path(path_lis))
    slugged_item_name = path_lis[-1][0:-5]
    items = get_all(container_obj)
    for item in items:
        if item.slug_name == slugged_item_name:
            return item
    return None


def path(item_obj, excl_item=False):
    """
    Get path of item, including item.
    Example: ['menu', 'fish.item']
    """
    container_obj = get_container(item_obj.container_id)
    path = container_obj.materialized_path
    if not excl_item:
        path += [item_obj.slug_name + ".item"]
    return path


def container(item_obj):
    """
    Get container object from item obj
    """
    return get_container(item_obj.container_id)


def slugify_item_name(item_obj):
    """
    Returns a slug-friend name (no spaces, special character, etC)
    for the item.

    Name should not clash with existing items in container.
    """
    slugged_name = __slugify(item_obj.name)
    items = get_all(get_container(item_obj.container_id))
    item_names = [x.slug_name for x in items]

    #check for dupes
    i = 2
    valid_slug = slugged_name
    while valid_slug in item_names:
        valid_slug = "%s1%d" % (slugged_name, i)
        i += 1

    return valid_slug


def __slugify(str):
    str = unidecode.unidecode(unicode(str)).lower()
    return re.sub(r'\W+', '-', str)


def move(item_obj, new_path_lis):
    pass


@schedulable
def save(item_obj):
    col = Item.collection()
    id = col.insert(item_obj.serialize())
    return id


def save_item(attr_dic, path_lis, publish_datetime=None):
    """
    Shortcut function to creating an item object.
    Returns item object.
    """
    container_obj = container_from_path(path_lis)
    if container_obj:
        container_obj = save_container_path(path_lis)
    if publish_datetime is None:
        publish_datetime = datetime.datetime.utcnow()

    #custom attr
    fields = Item.INCLUDED_FIELDS + Item.META_FIELDS
    keys = attr_dic.keys()
    not_part_of_fields = [x for x in keys if x not in fields]

    item_obj = Item(**attr_dic)
    item_obj.publish_datetime = publish_datetime
    item_obj.container_id = container_obj.obj_id()
    item_obj.slug_name = slugify_item_name(item_obj)
    item_obj.status = ItemStatus.VISIBLE
    item_obj.custom_attr_lis = not_part_of_fields
    item_obj._id = save(item_obj)
    return item_obj


#--- container functions ---

def move_container(container_obj, new_parent_path_lis):
    pass


def save_container(container_obj):
    col = Container.collection()
    id = col.insert(container_obj.serialize())
    return id


def save_container_path(container_path_lis):
    """
    Shortcut for creating containers.

    Creates the chain of container objects.
    Returns container object, not container id.
    """
    for i in range(1, len(container_path_lis) + 1):
        path = container_path_lis[:i]
        if not container_from_path(path):
            container_obj = Container()
            container_obj.slug_name = __slugify(path[-1])
            container_obj.name = path[-1]
            container_obj.materialized_path = path

            if i > 1:
                parent_obj = container_from_path(path[0:-1])
                container_obj.parent_id = parent_obj.obj_id()
            save_container(container_obj)

    return container_from_path(container_path_lis)


def get_container(container_id):
    """
    Given container id, return container object.
    None if nothing found.
    """
    coll = Container.collection()
    dic = coll.find_one({"_id": coerce_bson_id(container_id)})
    return Container.unserialize(dic) if dic is not None else None


def container_from_path(path):
    """
    Return container object from path, None if nothing found.
    """
    coll = Container.collection()
    dic = coll.find_one({"materialized_path": path})
    return Container.unserialize(dic) if dic is not None else None


def get_all(container_obj, find_param_lis=None, limit=None):
    """
    Get all items objects in a list given a container object.

    :param container_obj:
    :return list_of_items:
    """
    if find_param_lis is None:
        find_param_lis = []
    if limit is None:
        limit = 5

    coll = Item.collection()
    lis_of_dic = coll.find({"container_id": container_obj.obj_id()})
    lis_of_dic = coll.find({
        "$and": [
                    {"container_id": container_obj.obj_id()}
                ] + find_param_lis,
    }, limit=limit)
    return [Item.unserialize(x) for x in lis_of_dic]


def container_path(path_lis):
    """
    Returns the Container path list, if it already isn't.
    "/menu/restaurant/item.item" will return "/menu/restaurant/" in list repr
    """
    if path_lis[-1][-5:len(path_lis[-1])] != ".item":
        return path_lis
    return path_lis[:-1]