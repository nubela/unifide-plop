from base.util import coerce_bson_id
from orders.order.model import Order
from base import items
from ecommerce import discounts

def get(order_id):
    """
    Get item from id
    """
    coll = Order.collection()
    dic = coll.find_one({"_id": coerce_bson_id(order_id)})
    return Order.unserialize(dic) if dic is not None else None


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


def find_item_discount(item):
    all_discounts = discounts.get_all()
    all_discounts.sort(key=lambda x: x.timestamp_utc)
    for d in all_discounts:
        if d.discount_scope == discounts.DiscountScope.ITEM_ONLY:
            if item.id() == d.obj_id:
                item.before_discount = item.price
                item.price = get_discounted_price(item, d)
                return True
        if d.discount_scope == discounts.DiscountScope.CONTAINER_WIDE:
            if item.container_id == d.obj_id:
                item.before_discount = item.price
                item.price = get_discounted_price(item, d)
                return True


def get_discounted_price(item, d):
    return (float(item.price) * float((100 - d.discount_percentage) / 100)) if d.discount_percentage > 0 else float(item.price) - d.absolute_discounted_price


def total_price(order_obj, discount=True):
    """
    Calculates the total price of all the items before any credit/debit filters
    """
    price = 0
    for i in order_obj.items:
        item = items.get(i["obj_id"])
        if discount:
            find_item_discount(item)
        price += float(item.price) * i["quantity"]
    return price


def nett_price(order_obj, discount=True):
    """
    Calculates the total price of all the times after credit/debit filters
    """
    debit = sum(map(lambda x: x["amount"], order_obj.debits))
    credit = sum(map(lambda x: x["amount"], order_obj.credits))
    nett = total_price(order_obj, discount) - debit
    return nett + credit if nett > 0 else 0 + credit


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