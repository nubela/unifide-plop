def path_string(path_lis, separator=None):
    """
    Convert a path of list repr to a str representation
    """
    if separator is None:
        separator = "/"
    return separator.join(path_lis)


def path_list(path_str, separator=None):
    """
    Convert a path of str repr to a list representation
    """
    if separator is None:
        separator = "/"

    tokens = path_str.split(separator)
    tokens = tokens.filter(lambda x: x != "", tokens)
    return tokens