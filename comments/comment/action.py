from base.util import coerce_bson_id
from comments.comment.model import Comment


def comment(user_obj, comment_str, obj_id, coll_name):
    """
    Shortcut function for instantiating and commenting
    on an arbitrary object

    :param user_obj:
    :param comment_str:
    :param obj_id:
    :param coll_name:
    :return comment_obj_id:
    """
    comment_obj = Comment()
    comment_obj.user_id = user_obj.obj_id()
    comment_obj.comment = comment_str
    comment_str.coll_name = coll_name
    comment_obj.obj_id = coerce_bson_id(obj_id)
    return save(comment_obj)


def save(comment_obj):
    """
    Saves a comment object on the database

    :param comment_obj:
    """
    id = Comment.collection().insert(comment_obj.serialize())
    return id


def get_all(obj_id, collection_name, limit=None):
    """
    Get all comments on a given object

    :param obj_id:
    :param collection_name:
    :param limit:
    """
    comments = Comment.collection().find({
        "obj_id": coerce_bson_id(obj_id),
        "coll_name": collection_name
    })
    comment_obj_lis = [Comment.unserialize(x) for x in comments]
    return comment_obj_lis


def get(comment_id):
    """
    Return the comment object given the id

    :param comment_id:
    """
    dic = Comment.collection().find_one({
        "_id": coerce_bson_id(comment_id)
    })
    return Comment.unserialize(dic) if dic is not None else None