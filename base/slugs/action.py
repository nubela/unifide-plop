from base.slugs.model import Slug
import unidecode


def get_slug_w_attr(slugged_name, item_coll_name):
    dic = Slug.collection().find_one({
        "coll_name": item_coll_name,
        "name": slugged_name
    })
    return dic


def sluggify(string_to_slugify, item_id, item_coll_name):
    """
    Translates an object into a readable slug (for readability purposes)
    """
    possible_slug = Slug.collection().find_one({
        "coll_name": item_coll_name,
        "item_id": item_id
    })
    if possible_slug is not None:
        return possible_slug["name"]

    base_slugged_name = unidecode.unidecode(string_to_slugify)

    #ensure that this is unique
    i = 1
    slugged_name = base_slugged_name
    while get_slug_w_attr(slugged_name, item_coll_name):
        slugged_name = "%s-%d" % (base_slugged_name, i)
        i += 1

    #lets save it so we can retrieve it l8r on
    s = Slug()
    s.coll_name = item_coll_name
    s.item_id = item_id
    s.name = slugged_name
    s.save()

    return slugged_name


def unsluggify(slugged_name, item_coll_name, obj_class_ref):
    """
    Translates a slug into an object ID
    """
    slug_dic = get_slug_w_attr(slugged_name, item_coll_name)
    dic = obj_class_ref.collection().find_one({"_id": slug_dic["item_id"]})
    return obj_class_ref.unserialize(dic) if dic is not None else None