import orders


def dic_to_order(cart_dic, o):
    for k, v in cart_dic.items:
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