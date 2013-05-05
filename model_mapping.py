from base import items
import campaigns


COLLECTION_MAP = {
    "item": {
        "model": items.Item,
        "get": items.get,
    },
    "campaign": {
        "model": campaigns.Campaign,
        "get": campaigns.get,
    },
}