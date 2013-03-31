"""
This package deals with items for a business.

`Item` - What the hell is it?
----------------------------
An item is an arbitrary storage node for anything informational a business has.

Some examples include
* a restaurant menu item
* an item for sale in the web store
* a branch information

Dev Structure
-------------
Items are sorted just as is how files are sorted in folders. Analogous to this concept,
an item is to a file as to how `Containers` are to folders.

So yes, containers lie as a tree structure which contain unique items.

Path
----
We engaged the __materialized_path__ method in managing the entire tree structure.
Basically, this creates a string path like "/menu/entree/apple.item" which
represents its container structure and the item that it points to.

A path containing an item will always end with ".item".
Without ".item", it is a container path that points to a `Container`.

Examples:
- "/menu/entree/apple.item" -> Apple item in Entree container with a parent of Menu container.
- "/menu/entree" -> The Entree container

Path list
---------
To make managing things easier on a code level, there is a path package within items to
convert a string representation into a list representation.

For example:
"/menu/entree/apple.item" would be ["menu", "entree", "apple.item"]

The list representation is the recommended and default way for all functions to
work with paths on a code level.
"""

from base.items.action import *
from base.items.model import *