from base import items
from base.util import coerce_bson_id
from ecommerce import discounts, taxes, cashbacks, shipping, coupons


def apply_tax(order_obj):
    """
    Given an order, updates the order with prevailing tax rules
    onto the order's credit attribute.
    Then it returns
    """
    tax_rule = taxes.get()
    all_credits = order_obj.credits
    other_credit = filter(lambda x: x["coll_name"] != taxes.TaxRule.coll_name(), all_credits)

    if tax_rule is not None:
        order_obj.credits = other_credit + [{
                                                "obj_id": tax_rule._id,
                                                "coll_name": taxes.TaxRule.coll_name(),
                                                "amount": taxes.amount(tax_rule, order_obj),
                                            }]
    else:
        order_obj.credits = other_credit


def apply_discounts(order_obj):
    """
    Given an order, updates the order with prevailing discount rules
    onto the order's debit attribute
    """
    all_dedits = order_obj.debits
    other_debit = filter(lambda x: x["coll_name"] != discounts.Discount.coll_name(), all_dedits)
    all_discounts = discounts.get_all()
    valid_discounts = []
    for item_dic in order_obj.items:
        for d in all_discounts:
            item_obj = items.get(coerce_bson_id(item_dic["obj_id"]))
            if item_obj is None: continue
            if discounts.valid_on_item(d, item_obj):
                valid_discounts += [{
                                        "obj_id": d._id,
                                        "coll_name": discounts.Discount.coll_name(),
                                        "amount": discounts.discounted_value(item_obj.price, d),
                                    }]
                break
    order_obj.debits = other_debit + valid_discounts
    return valid_discounts


def apply_cashback(order_obj):
    all_dedits = order_obj.debits
    other_debit = filter(lambda x: x["coll_name"] != cashbacks.CashbackRule.coll_name(), all_dedits)
    cashback_rule = cashbacks.get()
    if cashback_rule is not None:
        order_obj.debits = other_debit + [{
                                              "obj_id": cashback_rule._id,
                                              "coll_name": cashbacks.CashbackRule.coll_name(),
                                              "amount": cashbacks.cashback_value(cashback_rule, order_obj),
                                          }]


def apply_shipping(order_obj, selected_shipping_method_id):
    avail_shipping_methods = shipping.get_all_valid(order_obj)
    print avail_shipping_methods
    all_credits = order_obj.credits
    other_credit = filter(lambda x: x["coll_name"] != shipping.ShippingRule.coll_name(), all_credits)

    #update shipping credit
    if len(avail_shipping_methods) > 0:
        #check if there is a submitted post
        if selected_shipping_method_id is not None and selected_shipping_method_id in map(lambda x: str(x._id),
                                                                                          avail_shipping_methods):
            rule_obj = filter(lambda x: str(x._id) == selected_shipping_method_id, avail_shipping_methods)[0]
            order_obj.credits = other_credit + [{
                                                    "obj_id": rule_obj._id,
                                                    "coll_name": shipping.ShippingRule.coll_name(),
                                                    "amount": shipping.cost(rule_obj, order_obj),
                                                }]
    else:
        order_obj.credits = other_credit
    return order_obj


def apply_coupon(order_obj, coupon_code, remove_coupon=False):
    #sane defaults
    if remove_coupon == "true":
        remove_coupon = True
    elif remove_coupon == "false":
        remove_coupon = False

    all_dedits = order_obj.debits
    other_debit = filter(lambda x: x["coll_name"] != coupons.Coupon.coll_name(), all_dedits)
    coupon_debit = filter(lambda x: x["coll_name"] == coupons.Coupon.coll_name(), all_dedits)

    coupon_obj = coupons.get_by_attr(coupon_code)

    if remove_coupon:
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