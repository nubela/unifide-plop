from base import items
from base.items import Item
from base.org import ORG_PATH
from base.org.model import OrgInfo


def get():
    """
    Returns a populated `OrgInfo` object
    """
    org_info = OrgInfo()
    container_obj = __get_or_create_org_container()
    all_org_items = items.get_all(container_obj)
    for k, v in vars(OrgInfo).items():
        if k[:2] != "__": #not a private attr
            attr_name = getattr(OrgInfo, k)
            item = __has_item(all_org_items, attr_name)
            if item:
                setattr(org_info, attr_name, item.description)
    return org_info


def __get_or_create_org_container():
    container_obj = items.container_from_path(ORG_PATH)
    if container_obj is None:
        items.save_container_path([ORG_PATH])
        container_obj = items.container_from_path(ORG_PATH)
    return container_obj


def save(org_info_obj):
    """
    Saves `OrgInfo` object
    """
    container_obj = __get_or_create_org_container()
    all_org_items = items.get_all(items.container_from_path(ORG_PATH))
    for k, v in vars(org_info_obj).items():
        existing_item = __has_item(all_org_items, k)
        if existing_item:
            if existing_item.description != v:
                existing_item.description = v
                items.save(existing_item)
        else:
            container_obj = items.container_from_path(ORG_PATH)
            item_obj = Item.unserialize({
                "name": k,
                "description": v,
                "container_id": container_obj.obj_id(),
            })
            items.save(item_obj)


def __has_item(item_list, key):
    for i in item_list:
        if i.name == key:
            return i
    return None