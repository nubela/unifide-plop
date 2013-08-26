from base import items
from ecommerce.coupons.action import CouponScope, CouponLifetime, CouponUserScope, CouponStatus
from ecommerce.coupons.model import Coupon
import loremipsum


def new_item_coupon(coupon_code, value, obj_id):
    c = Coupon()
    c.coupon_scope = CouponScope.ITEM_ONLY
    c.coll_name = items.Item.coll_name()
    c.obj_id = obj_id
    c.coupon_code = coupon_code
    c.coupon_value = value
    c.valid_times = 1
    c.coupon_lifetime_type = CouponLifetime.FOREVER
    c.user_scope = CouponUserScope.ALL
    c.name = loremipsum.sentence()
    c.description = loremipsum.paragraph()
    c.status = CouponStatus.AVAILABLE
    c.save()


def new_container_coupon(coupon_code, value, container_id):
    c = Coupon()
    c.coupon_scope = CouponScope.CONTAINER_WIDE
    c.coll_name = items.Container.coll_name()
    c.obj_id = container_id
    c.coupon_code = coupon_code
    c.coupon_value = value
    c.valid_times = 1
    c.coupon_lifetime_type = CouponLifetime.FOREVER
    c.user_scope = CouponUserScope.ALL
    c.name = loremipsum.sentence()
    c.description = loremipsum.paragraph()
    c.status = CouponStatus.AVAILABLE
    c.save()