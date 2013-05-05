from random import choice
import loremipsum
from base import items, users
from orders import save, Order, OrderStatus


GEN_ITEM_PATH_LIS = ["Order Mock"]


def gen_items(total_items=5):
    container_obj = items.container_from_path(GEN_ITEM_PATH_LIS)
    if container_obj is None:
        container_obj = items.save_container_path(GEN_ITEM_PATH_LIS)

    item_lis = []
    for _ in range(total_items):
        dic = {
            "name": loremipsum.sentence(max_char=choice(range(10, 20))),
            "media": None,
            "description": loremipsum.paragraph(max_char=choice(range(40, 100))),
            "quantity": choice(range(1, 20)),
            "price": choice(range(1, 20)),
            "container_id": container_obj.obj_id(),
        }
        item_obj = items.Item.unserialize(dic)
        item_obj._id = items.save(item_obj)
        item_lis += [item_obj]

    return item_lis


def gen_users(total_users=10):
    user_lis = []
    for _ in range(total_users):
        dic = {
            "first_name": "Nubela",
            "last_name": "Steven",
            "email": "blabla@bla.com",
            "account_status": users.AccountStatus.ENABLED,
        }
        user_obj = users.User.unserialize(dic)
        user_obj._id = users.save(user_obj)
        user_lis += [user_obj]
    return user_lis


def gen_orders(user_lis, item_lis, total_orders=50):
    for _ in range(total_orders):
        random_item = choice(item_lis)
        random_user = choice(user_lis)
        dic = {
            "user_id": random_user.obj_id(),
            "obj_id": random_item.obj_id(),
            "coll_name": "item",
            "quantity": choice(range(1, 2)),
            "special_notes": loremipsum.sentence(),
            "status": OrderStatus.OK,
        }
        order_obj = Order.unserialize(dic)
        save(order_obj)


def mock_and_save():
    print "Mocking orders.."
    gen_orders(gen_users(), gen_items())
    print "Done mocking orders"