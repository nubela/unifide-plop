from random import choice
from articles import ARTICLE_PATH
from articles.default_config import MOCK_DATE_RANGE_DAYS
from base import items
from base.items import save_container_path
from base.util import __gen_random_datetime
import loremipsum

def gen_article_path():
    save_container_path(ARTICLE_PATH)


def gen_articles(total_items=20):
    for _ in range(total_items):
        basic_attr = {
            "name": loremipsum.sentence(max_char=choice(range(10, 20))),
            "image": None,
            "description": loremipsum.paragraph(),
        }
        publish_datetime = __gen_random_datetime(MOCK_DATE_RANGE_DAYS)
        items.save_item(basic_attr, ARTICLE_PATH, publish_datetime)


def mock_and_save():
    print "Mocking articles.."
    gen_article_path()
    gen_articles()
    print "Done mocking articles"
