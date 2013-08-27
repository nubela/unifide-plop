import datetime
from decimal import Decimal
from base import users, items
from ecommerce.coupons.model import CouponLog, Coupon
import orders


def _log(order_obj, coupon):
    l = CouponLog()
    l.used_date_utc = datetime.datetime.utcnow()
    l.user_id = order_obj.user_id
    l.order_id = order_obj._id
    l.discounted_total = coupon_discount_price(coupon, order_obj)
    return l.save()


def apply_coupon(order_obj, coupon):
    """
    """
    #todo
    _log(order_obj, coupon)


def get_by_attr(coupon_code):
    dic = Coupon.collection().find_one({"coupon_code": coupon_code})
    return Coupon.unserialize(dic) if dic is not None else None


def _general_discount(coupon, order_obj):
    total_price = orders.total_price(order_obj)
    if total_price >= coupon.coupon_value:
        return Decimal(coupon.coupon_value)
    else:
        return Decimal(total_price)


def _container_discount(coupon, order_obj):
    all_items = order_obj.items # {obj_id: None, coll_name: None, quantity:None}
    total_price = 0
    coupon_container = items.get_container(coupon.obj_id)
    for i in all_items:
        item = items.get(i["obj_id"])
        item_container = items.item_container(item)
        if item_container._id == coupon.obj_id or items.parent_container(coupon_container, item_container):
            total_price += (item.price * i["quantity"])

    if total_price >= coupon.coupon_value:
        return Decimal(coupon.coupon_value)
    else:
        return Decimal(total_price)


def _item_discount(coupon, order_obj):
    all_items = order_obj.items # {obj_id: None, coll_name: None, quantity:None}
    for i in all_items:
        if i["obj_id"] == coupon.obj_id:
            item = items.get(i["obj_id"])
            total_price = item.price * i["quantity"]
            if total_price >= coupon.coupon_value:
                return Decimal(coupon.coupon_value)
            else:
                return Decimal(total_price)


def coupon_discount_price(coupon, order_obj):
    if coupon.coupon_scope == CouponScope.CONTAINER_WIDE:
        return _container_discount(coupon, order_obj)
    elif coupon.coupon_scope == CouponScope.ITEM_ONLY:
        return _item_discount(coupon, order_obj)
    else:
        return _general_discount(coupon, order_obj)


def is_valid(coupon, order_obj):
    """
    Checks if a coupon is valid on an order
    """
    user_obj = users.get(order_obj.user_id)
    user_groups = user_obj.groups
    utc_now = datetime.datetime.utcnow()
    order_price = orders.total_price(order_obj)
    if coupon.user_scope == CouponUserScope.GROUP:
        if coupon.user_group not in user_groups:
            return False
    if coupon.user_scope == CouponUserScope.SPECIFIC:
        if coupon.user_id != user_obj._id:
            return False
    if coupon.valid_times <= 0:
        return False
    if coupon.coupon_lifetime_type == CouponLifetime.LIMITED:
        if utc_now > coupon.expire_utc_datetime:
            return False
        if utc_now < coupon.begins_utc_datetime:
            return False
    if coupon.order_minimum_spending < order_price:
        return False

    all_items = order_obj.items # {obj_id: None, coll_name: None, quantity:None}

    flag = False
    for i in all_items:
        i["obj"] = items.get(i["obj_id"])
        i["container"] = items.item_container(i["obj"])

        if coupon.coupon_scope == CouponScope.CONTAINER_WIDE:
            container_obj = items.get_container(coupon.obj_id)
            if items.is_parent_container(container_obj, i["container"]) or i["container"]._id == coupon.obj_id:
                flag = True
                break

        if coupon.coupon_scope == CouponScope.ITEM_ONLY:
            if i["obj_id"] == coupon.obj_id:
                flag = True
                break
    if not flag: return False

    return True


class CouponLifetime:
    FOREVER = "forever"
    LIMITED = "limited"


class CouponUserScope:
    ALL = "all"
    GROUP = "user_group"
    SPECIFIC = "specific_user"


class CouponStatus:
    AVAILABLE = "available"
    DISABLED = "disabled"


class CouponScope:
    CONTAINER_WIDE = "container_wide"
    ITEM_ONLY = "item_only"
    ALL_ITEMS = "all"