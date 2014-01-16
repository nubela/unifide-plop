from ecommerce import cart, coupons
from flask import request, session, jsonify
from flask.ext.login import current_user
import orders


#-- plop utils --#

def _update_coupon(order_obj):
    all_dedits = order_obj.debits
    other_debit = filter(lambda x: x["coll_name"] != coupons.Coupon.coll_name(), all_dedits)
    coupon_debit = filter(lambda x: x["coll_name"] == coupons.Coupon.coll_name(), all_dedits)

    coupon_code = request.form.get("coupon_code")
    remove_coupon = request.form.get("remove_coupon")
    coupon_obj = coupons.get_by_attr(coupon_code)

    if remove_coupon == "true":
        order_obj.debits = other_debit
        coupon_debit = []
    elif coupon_obj is not None:
        coupon_debit = [{
                            "obj_id": coupon_obj._id,
                            "coll_name": coupons.Coupon.coll_name(),
                            "amount": coupon_obj.coupon_value,
                        }]
        order_obj.debits = other_debit + coupon_debit
    return coupon_debit


def _update_user(order_obj):
    """
    Updates the order object with the current user logined
    """
    if current_user is not None and not current_user.is_anonymous():
        order_obj.user_id = current_user._id


def _session_to_order():
    """
    Converts a JSON key/val in session into an order (if it exists)
    """
    order_obj = None
    if "current_order" not in session:
        cart_dic = session[cart.CartType.SHOPPING] if cart.CartType.SHOPPING in session else {}
        order_obj = cart.to_order(cart_dic)
    else:
        cart_dic = session[cart.CartType.SHOPPING] if cart.CartType.SHOPPING in session else {}
        order_obj = orders.Order.unserialize(session["current_order"])
        cart.dic_to_order(cart_dic, order_obj)

    #append user_id to order
    if current_user is not None and not current_user.is_anonymous():
        order_obj.user_id = current_user._id

    return order_obj


def _order_to_session(order_obj):
    """
    Util method to convert an order object into a JSON to be saved in session.
    """
    session["current_order"] = order_obj.serialize(json_friendly=True)


def _post_or_get(key, default_val=None):
    """
    Gets a value from either FORM or ARGS, with precedence from FORM.
    """
    return request.form.get(key, request.args.get(key, default_val))

#-- endpoints methods --#

def add_to_cart():
    cart_name = _post_or_get("cart_name")
    item_id = _post_or_get("item_id")
    qty = int(_post_or_get("quantity", 1))
    if None in (cart_name, item_id, qty):
        return jsonify({
            "status": "error",
        })

    if cart_name not in session:
        session[cart_name] = {}
    if item_id in session[cart_name]:
        session[cart_name][item_id] = qty
    else:
        session[cart_name][item_id] = qty

    return jsonify({
        "status": "ok",
        "cart": session[cart_name],
    })


def rm_from_cart():
    cart_name = _post_or_get("cart_name")
    item_id = _post_or_get("item_id")

    if None in (cart_name, item_id):
        return jsonify({
            "status": "error",
        })

    if cart_name not in session:
        session[cart_name] = {}

    #remove item from the session cart
    if item_id in session[cart_name]:
        del session[cart_name][item_id]

    #remove the item from the order as well
    order_obj = None
    if "current_order" not in session:
        cart_dic = session[cart.CartType.SHOPPING] if cart.CartType.SHOPPING in session else {}
        order_obj = cart.to_order(cart_dic)
    else: order_obj = orders.Order.unserialize(session["current_order"])
    cart.dic_to_order(session[cart_name], order_obj)
    session["current_order"] = order_obj.serialize(json_friendly=True)

    return jsonify({
        "status": "ok",
        "cart": session[cart_name],
    })