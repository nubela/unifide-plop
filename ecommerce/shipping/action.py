from base import items
from base.util import coerce_bson_id
from ecommerce.shipping.model import ShippingRule


def get(shipping_rule_id):
    dic = ShippingRule.collection().find_one({
        "_id": coerce_bson_id(shipping_rule_id),
    })
    return ShippingRule.unserialize(dic) if dic is not None else None

def get_all():
    dic_lis = ShippingRule.collection().find({
        "status": ShippingStatus.ENABLED
    })
    return map(lambda x: ShippingRule.unserialize(x), dic_lis)


def _order_weight(order_obj):
    total_weight = 0
    for i in order_obj.items:
        item_obj = items.get(i["obj_id"])
        if hasattr(item_obj, "weight") and item_obj.weight is not None:
            try:
                total_weight += float(item_obj.weight) * float(i['quantity'])
            except ValueError:
                pass
    return total_weight


def get_all_valid(order_obj, ship_to=None):
    """
    Get all shipping rules that are valid for a specific order
    """
    all_shipping_rules = get_all()
    valid_shipping_rules = []
    total_weight = _order_weight(order_obj)

    for s in all_shipping_rules:
        #location requirements
        fail_requirements = False
        if s.to_location is not None and ship_to is not None and s.to_location.lower() != ship_to.lower():
            continue
        if s.from_location is not None:
            for i in order_obj.items:
                item = items.get(i["obj_id"])
                if hasattr(item, "location") and getattr(item, "location") != s.from_location:
                    fail_requirements = True
                    break
        if fail_requirements:
            continue

        #weight requirements
        if float(s.min_unit_vol_weight) > total_weight:
            #continue
            pass
        if float(s.max_unit_vol_weight) < total_weight:
            continue

        #add it
        valid_shipping_rules += [s]

    return valid_shipping_rules


def cost(shipping_rule, order_obj):
    if order_obj is None or shipping_rule is None: return 0
    total_weight = _order_weight(order_obj)
    if total_weight == 0:
        return float(shipping_rule.flat_price)
    return float((total_weight * shipping_rule.price_per_unit_vol_weight) + shipping_rule.flat_price)


class ShippingStatus:
    ENABLED = "enabled"
    DISABLED = "disabled"


class ShippingPriceType:
    FLAT = "flat"
    WEIGHT_BASED = "weight_based"