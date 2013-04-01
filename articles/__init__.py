"""
This package handles persistent information, in the form of articles.

How is this different from `items` package?
------------------------------------------

The article's package is not too different from items package. In fact, it uses it.
This package is in fact a __syntactic_sugar__  to the items package.

We use a fixed path, specifically "/Articles/" to store the article items.


How is this different from `campaigns` package?
----------------------------------------------

A campaign is a temporal thing, like an event. It happens one time and expires away into oblivion.
An article is persistent, and is more prose-oriented, rather than item/picture/event.

"""
ARTICLE_PATH = ["Articles"]
from articles.article.action import *