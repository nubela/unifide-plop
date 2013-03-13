from base.base_model import Base


class Item(Base):
    def __init__(self):
        self.name = None
        self.description = None
        self.price = None
        self.release_date = None