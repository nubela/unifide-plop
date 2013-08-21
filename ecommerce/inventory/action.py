from base import items
from ecommerce.inventory.model import Inventory


def all_inventorized_containers():
    all_inventory = Inventory.collection().find()
    containers = []
    for i in all_inventory:
        containers += [items.get_container(i["container_id"])]
    return containers


def add_to_inventory(container_id):
    i = Inventory()
    i.container_id = container_id
    return i.save()


def warnings(min_qty):
    """
    Return items that are <= min_qty
    """
    warning_items = []
    for c in all_inventorized_containers():
        items = items.get_all(c)
        for i in items:
            if hasattr(i, "quantity") and i.quantity <= min_qty:
                warning_items += [i]
    return warning_items