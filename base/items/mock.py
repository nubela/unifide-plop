from random import choice
from base import items
from base.items import save_container_path, Item, container_from_path
import loremipsum


class Generate:
    ITEMS_CONTAINERS = "items_containers"
    ITEMS_ONLY = "items"


class ContainerAttr:
    DISCOUNT_PERCENTAGE = "discount_perc"
    DISCOUNT_ABSOLUTE = "discount_abs"
    INSTRUCTIONS = "instructions"
    DESCRIPTION = "description"


class ItemAttr:
    INSTRUCTIONS = "instructions"


def _spawn_items_containers(pl):
    containers_to_cr8 = [loremipsum.sentence(30) for _ in range(choice(range(1, 3)))]
    all_pl = map(lambda x: pl + [x], containers_to_cr8)
    items_to_cr8 = [loremipsum.sentence(30) for _ in range(choice(range(5, 10)))]

    for item_name in items_to_cr8:
        i = Item()
        i.name = item_name
        i.description = loremipsum.paragraph()
        i.price = choice(range(1, 100))
        i.container_id = container_from_path(pl)._id
        i.save()
    for container_pl_to_cr8 in all_pl:
        save_container_path(container_pl_to_cr8)
    return all_pl


def _spawn_items(pl):
    items_to_cr8 = [loremipsum.sentence(30) for _ in range(choice(range(10, 20)))]
    all_items = []
    for item_name in items_to_cr8:
        i = Item()
        i.name = item_name
        i.description = loremipsum.paragraph()
        i.price = choice(range(1, 100))
        i.container_id = container_from_path(pl)._id
        i._id = i.save()
        all_items += [i]
    return all_items


def gen_model(model, existing_path_lis=None):
    if existing_path_lis is None: existing_path_lis = []

    if Generate.ITEMS_CONTAINERS == model:
        max_depth = choice(range(1, 3))
        to_gen = _spawn_items_containers(existing_path_lis)
        for g in to_gen:
            depth = len(g) - len(existing_path_lis)
            if depth > max_depth: break
            to_gen += _spawn_items_containers(g)
        return

    for container_name, attr_dic in model.items():
        #save container
        path_lis = existing_path_lis + [container_name]

        #only create if container doesnt already exists
        if items.container_from_path(path_lis) is None:
            container_obj = save_container_path(path_lis)
            if ContainerAttr.DESCRIPTION in model: container_obj.description = model[ContainerAttr.DESCRIPTION]
            container_obj.save()

            #create items
            if "items" in model:
                for item in model["items"]:
                    custom_type = item["custom"] if "custom" in item else None
                    if custom_type is None:
                        i = Item(**{item})
                        i.container_id = container_from_path(existing_path_lis)
                        i.save()
                    elif custom_type == Generate.ITEMS_ONLY:
                        all_items = _spawn_items(existing_path_lis)
                        custom_attr = item["custom_attr"] if "custom_attr" in item else {}
                        for k, v in custom_attr:
                            for new_item in all_items:
                                setattr(new_item, k, v)
                        map(lambda x: x.save(), all_items)

        #gen recursive models
        if "containers" in attr_dic:
            gen_model(attr_dic["containers"], path_lis)