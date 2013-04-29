"""
[This package has special instructions]

This is the base package that does image support at its basic level.
By image support, I really mean uploading, parsing urls, and managing their storage presence.

Special management of models
----------------------------
The `Image` model can and __should__ be stored as a JSON embedded in other models. Simply because we don't want
every image access to read the database once.

This means, the primary use case of the action layer is to write, and not read.

Package purpose
---------------
This package seeks to backlog all images in a central location.
"""
from base.media.action import *
from base.media.model import *