import datetime
from base import scheduling
from base.scheduling.decorator import schedulable
from bson.objectid import ObjectId
from orders.order.model import Order, StockAvailability

def save(user_obj, collection_name, item_id):
    """
    Confirms and saves an order of an item
    """
    order_obj = Order()
    order_obj.obj_id = item_id
    order_obj.user_id = user_obj.id()
    order_obj.coll_name = collection_name

    id = Order.collection().insert(order_obj.serialize())
    return id


def remove(user_obj, collection_name, item_id):
    """
    Removes an order of an item
    """
    order_obj = get_order_by_attr(**{
        "obj_id": item_id,
        "user_id": user_obj.id,
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
        "_id": ObjectId(str(order_id))
    })
    return Order.unserialize(dic) if dic is not None else None


def get_order_by_attr(**kwargs):
    dic = Order.collection().find_one(kwargs)
    return Order.unserialize(dic)  if dic is not None else None


@schedulable
def set_availability(obj_id, collection_name, stock_quantity, publish_datetime):
    stock = StockAvailability()
    stock.obj_id = obj_id
    stock.coll_name = collection_name
    stock.availability = stock_quantity
    stock.publish_datetime_utc = publish_datetime
    id = StockAvailability.collection().insert(stock.serialize())
    return id


def available(obj_id, collection_name):
    """
    Get all stock availability published up to now,
    and then the count of all the orders for this object.
    Returns the leftover.
    """
    stocks = scheduling.get_before(StockAvailability, datetime.datetime.utcnow(), limit=None)
    total_avail = sum([x.availability for x in stocks])
    orders = Order.collection().find({"obj_id": "obj_id", "coll_name": collection_name}).count()
    return total_avail - orders