import json
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
drink_file = os.path.join(THIS_FOLDER, './../../data/drink_price.json')

with open(drink_file) as f:
    drink_price = json.load(f)

class Drink:
    """ A drink in pizza parlour order.

    === Attributes ===
    name: name of the drink
    price: price of the drink
    """
    name: str
    price: float

    def __init__(self, name: str):
        """Initialize a new Drink object given its name
        Precondition: name is one of coke, diet coke, coke zero, pepsi, diet pepsi, dr.pepper, water, juice."""
        self.name = name
        self.price = drink_price[name]
