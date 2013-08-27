from base import users


def gen_groups(dic):
    for group_name, desc in dic.items():
        if users.get_group_name(group_name) is None:
            users.new_group(group_name, desc)