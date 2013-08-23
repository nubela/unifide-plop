from orders.order.model import Order
from base import items


def new(user_id):
    o = Order()
    o.user_id = user_id
    o.status = OrderStatus.NEW
    return o


def update_status(order_obj, status):
    order_obj.status = status
    return order_obj


def add_item(order_obj, item_obj, quantity):
    remove_item(order_obj, item_obj, quantity)
    order_obj.items += [{"obj_id": order_obj._id, "coll_name": items.Item.coll_name(), "quantity": quantity}]
    return order_obj


def remove_item(order_obj, item_obj):
    return filter(lambda x: x["obj_id"] != item_obj._id, order_obj.items)


def total_price(order_obj):
    """
    Calculates the total price of all the items before any credit/debit filters
    """
    price = 0
    for i in order_obj.items:
        item = items.get(i["obj_id"])
        price += item.price * i["quantity"]
    return price


def nett_price(order_obj):
    """
    Calculates the total price of all the times after credit/debit filters
    """
    pass


def append_credit(order_obj, credit_obj):
    """
    {obj_id: None, coll_name: None, amount=None}
    """
    order_obj.credit += [credit_obj]
    return order_obj


def append_debit(order_obj, debit_obj):
    order_obj.debit += [debit_obj]
    return order_obj


class OrderStatus:
    SHIPPED = "Shipped"
    PROCESSING = "Processing"
    NEW = "New"
    CANCELLED = "Cancelled"
    HOLD = "On Hold"