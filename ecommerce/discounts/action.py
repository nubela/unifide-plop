from decimal import Decimal
import datetime
from base import items
import orders


def is_item_scoped(discount, item_obj):
    if item_obj.discount_scope == DiscountScope.ALL_ITEMS:
        return True
    if discount.collection_name != items.Item.coll_name():
        return False
    if item_obj._id != discount.obj_id:
        return False
    return True


def is_container_scoped(discount, container_obj):
    if container_obj.discount_scope == DiscountScope.ALL_ITEMS:
        return True
    if discount.collection_name != items.Container.coll_name():
        return False
    if container_obj._id != discount.obj_id and not items.is_parent_container(items.get_container(discount.obj_id), container_obj):
        return False
    return True


def valid_on_item(discount, item_obj):
    """
    Checks if a discount is valid on an item.
    """
    item_container = items.item_container(item_obj)
    if discount.discount_scope == DiscountScope.ORDER:
        return False
    if not is_item_scoped(discount, item_obj) and is_container_scoped(discount, item_container):
        return False
    utc_now = datetime.datetime.utcnow()
    if item_obj.price <= discount.item_minimum_spending:
        return False
    if discount.discount_lifetime_type == DiscountLifetime.LIMITED:
        if discount.expire_utc_datetime is not None and utc_now > discount.expire_utc_datetime:
            return False
        if discount.begins_utc_datetime is not None and utc_now < discount.begins_utc_datetime:
            return False
    if discount.status == DiscountStatus.DISABLED:
        return False
    return True


def valid_on_order(discount, order_obj):
    if discount.discount_scope != DiscountScope.ORDER:
        return False
    utc_now = datetime.datetime.utcnow()
    if orders.total_price(order_obj) <= discount.order_minimum_spending:
        return False
    if discount.discount_lifetime_type == DiscountLifetime.LIMITED:
        if discount.expire_utc_datetime is not None and utc_now > discount.expire_utc_datetime:
            return False
        if discount.begins_utc_datetime is not None and utc_now < discount.begins_utc_datetime:
            return False
    if discount.status == DiscountStatus.DISABLED:
        return False
    return True


def discounted_price(price, discount):
    """
    Disregarding the validity of the discount, fetches the price after a discount is applied on the price.
    """
    price = price - discount.absolute_discounted_price
    price = Decimal(price) * Decimal(discount.discount_percentage) / Decimal(100)
    return price


def get_item_price(item_obj, discount):
    """
    Fetches the price of item after discount
    """
    if not isinstance(item_obj.price, (int, long, float, complex)):
        return item_obj.price

    if not valid_on_item(discount, item_obj):
        return item_obj.price

    return discounted_price(item_obj.price, discount)


def get_order_price(order_obj, discount):
    """
    Fetches the price of the order after discount
    """
    if not valid_on_order(discount, order_obj):
        return order_obj.price

    return discounted_price(orders.total_price(order_obj), discount)


class DiscountScope:
    CONTAINER_WIDE = "container_wide"
    ITEM_ONLY = "item_only"
    ALL_ITEMS = "all"
    ORDER = "order"


class DiscountLifetime:
    FOREVER = "forever"
    LIMITED = "limited"


class DiscountStatus:
    ENABLED = "enabled"
    DISABLED = "disabled"