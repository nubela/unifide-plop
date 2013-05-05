from base.util import coerce_bson_id
from orders.order.model import Order


def save(order_obj):
    """
    Confirms and saves an order of an item
    """
    return Order.collection().save(order_obj.serialize())


def remove(user_obj, collection_name, item_id):
    """
    Removes an order of an item
    """
    order_obj = get_order_by_attr(**{
        "obj_id": coerce_bson_id(item_id),
        "user_id": user_obj.obj_id(),
        "collection_name": collection_name,
    })
    Order.collection().remove({
        "_id": order_obj.obj_id()
    })


def get(order_id):
    """
    Gets an order object given its id
    """
    dic = Order.collection().find_one({
        "_id": coerce_bson_id(order_id),
    })
    return Order.unserialize(dic) if dic is not None else None


def get_order_by_attr(**kwargs):
    dic = Order.collection().find_one(kwargs)
    return Order.unserialize(dic) if dic is not None else None


class OrderStatus:
    SHIPPED = "Shipped"
    PROCESSING = "Processing"
    OK = "New" #or rsvped if it is for events
    CANCELLED = "Cancelled"
    HOLD = "On Hold"