"""
This is a tagging package designed to tag any objects.

Tagging should be used for when items (or any other objs) belong to more than 1 category.
(And hence not able to fit in a tree structure)

Example:
`Coca cola` can be under "Drinks" and "Cola products". In this case, the object will have the 2
following tags.

Tags are inherently flat and have no hierachy.
"""
from base.tagging.action import *
from base.tagging.model import *