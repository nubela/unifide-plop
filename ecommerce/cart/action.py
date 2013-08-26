import orders
from  base import items


def dic_to_order(cart_dic, o):
    o.items = []
    for k, v in cart_dic.items():
        if items.get(k) is not None:
            o.items += [{"obj_id": k, "quantity": v}]


def to_order(cart_dic):
    """
    Converts a session's cart dictionary to an order object.
    """
    o = orders.Order()
    o.status = orders.OrderStatus.NEW
    dic_to_order(cart_dic, o)
    return o


class CartType:
    SHOPPING = "shopping"
    WISHLIST = "wishlist"