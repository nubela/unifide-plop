from base import items
from base.items.mock import ContainerAttr
from ecommerce.discounts import Discount, DiscountLifetime, DiscountStatus
import loremipsum


def gen_discounts(model, existing_path_lis=[]):
    """
    Generate discounts for individual containers from a model
    """
    if existing_path_lis is None: existing_path_lis = []

    for container_name, attr_dic in model.items():
        path_lis = existing_path_lis + [container_name]
        container_obj = items.container_from_path(path_lis)

        discount_obj = Discount()
        discount_obj.coll_name = items.Container.coll_name()
        discount_obj.obj_id = container_obj._id
        discount_obj.discount_lifetime_type = DiscountLifetime.FOREVER
        discount_obj.name = loremipsum.sentence(max_char=30)
        discount_obj.description = loremipsum.paragraph()
        discount_obj.status = DiscountStatus.ENABLED

        if ContainerAttr.DISCOUNT_PERCENTAGE in attr_dic:
            perc = attr_dic[ContainerAttr.DISCOUNT_PERCENTAGE]
            discount_obj.discount_percentage = perc
            discount_obj.save()

        if ContainerAttr.DISCOUNT_ABSOLUTE in attr_dic:
            amount = attr_dic[ContainerAttr.DISCOUNT_ABSOLUTE]
            discount_obj.absolute_discounted_price = amount
            discount_obj.save()

        #gen recursive models
        if "containers" in model: gen_discounts(model["containers"], path_lis)