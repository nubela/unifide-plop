import datetime
from articles import ARTICLE_PATH
from base import items


def __container_obj():
    return items.container_from_path(ARTICLE_PATH)


def get_published_articles(limit=3):
    articles = items.get_all(__container_obj(), find_param_lis=[
        {"publish_datetime": {"$lt": datetime.datetime.utcnow()}}
    ], limit=limit)
    return articles


def save_article(attr_dic):
    return items.save_item(attr_dic, ARTICLE_PATH)