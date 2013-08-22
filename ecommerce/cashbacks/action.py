from decimal import Decimal
from ecommerce.cashbacks.model import CashbackRule, CreditLog, CreditStore
import orders


def _log(admin_id, user_id, cashback_rule=None, order_id=None, value=None, ltype=None):
    c = CreditLog()
    c.admin_id = admin_id
    c.user_id = user_id
    c.cashback_rule_id = cashback_rule._id
    c.order_id = order_id
    c.credited_value = value
    c.type = ltype
    return c.save()


def get_store(user_id):
    dic = CreditStore.collection().find_one({"user_id": user_id})
    return CreditLog.unserialize(dic) if dic is not None else None


def give(admin_id, user_id, amount):
    store = get_store(user_id)
    if store is None: store = new_store(user_id)
    store.total_credit += amount
    store.save()
    _log(admin_id, user_id, ltype=CreditLogType.GIVE, value=amount)
    return store


def debit(admin_id, user_id, order_id, amount):
    store = get_store(user_id)
    if store is not None and store.total_credit >= amount:
        store.total_credit -= amount
        store.save()
        _log(admin_id, user_id, order_id=order_id, ltype=CreditLogType.DEBIT, value=amount)
    return store


def new_store(user_id):
    store = CreditStore()
    store.user_id = user_id
    store.save()
    return store


def credit(admin_id, user_id, order_obj, cashback_rule):
    amount = cashback_value(cashback_rule, order_obj)
    store = get_store(user_id)
    if store is None: store = new_store(user_id)

    store.total_credit += amount
    store.save()

    _log(admin_id, user_id, cashback_rule=cashback_rule, order_id=order_obj._id, value=amount,
         ltype=CreditLogType.CREDIT)
    return store


def reversal(admin_id, user_id, order_obj, cashback_rule):
    amount = cashback_value(cashback_rule, order_obj)
    store = get_store(user_id)

    store.total_credit -= amount
    store.save()

    _log(admin_id, user_id, cashback_rule=cashback_rule, order_id=order_obj._id, value=amount,
         ltype=CreditLogType.REVERSAL)
    return store


def cashback_value(cashback_rule, order_obj):
    price = orders.total_price(order_obj)
    price = Decimal(price) * Decimal(cashback_rule.cashback_percentage) / Decimal(100)
    return price


def get():
    dic = CashbackRule.collection().find_one({
        "status": CashbackStatus.ENABLED,
    })
    return CashbackRule.unserialize(dic) if dic is not None else None


class CreditLogType:
    DEBIT = "debit"
    CREDIT = "credit"
    REVERSAL = "reversal"
    GIVE = "give"


class CashbackStatus:
    ENABLED = "enabled"
    DISABLED = "disabled"