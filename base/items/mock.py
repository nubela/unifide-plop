from random import choice

import loremipsum

from base.items import save_item, save_container_path


def mock_and_save():
    print "Mocking items.."
    gen_paths()
    gen_items()
    print "Done mocking items"


def gen_items(total_items=100):
    """
    Generate items, duh.
    """
    for _ in range(total_items):
        basic_attr = {
            "name": loremipsum.sentence(max_char=choice(range(10, 20))),
            "image": None,
            "description": loremipsum.paragraph(),
            "price": choice(range(1, 100)),
        }

        path_lis = choice(__generated_paths())
        save_item(basic_attr, path_lis)


def __generated_paths():
    paths = [
        ["Menu", "Food", "Starters"],
        ["Menu", "Food", "Mains"],
        ["Menu", "Food", "Desserts"],
        ["Branches"],
    ]
    return paths


def gen_paths():
    paths = __generated_paths()
    for p in paths:
        save_container_path(p)