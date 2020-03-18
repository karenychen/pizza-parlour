from typing import Dict, List, Optional
from PizzaType import PizzaFactory, PizzaType
import json
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
size_file = os.path.join(THIS_FOLDER, './../../data/size_price.json')

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
topping_file = os.path.join(THIS_FOLDER, './../../data/topping_price.json')

# load sizes
with open(size_file) as f:
    size = json.load(f)

# load topping prices
with open(topping_file) as f:
    topping_price = json.load(f)

class Pizza:
    """ A Pizza class.

    === Attributes ===
    size: size of the pizza, can be either "small", "medium", "large" or "xlarge"
    type: type of the pizza
    toppings: a dictionary with all the additional toppings
    price: price of the pizza
    """
    size: str
    type: PizzaType
    toppings: Dict[str, int]
    price: float
    
    def __init__(self, size: str, type: str, toppings: Dict[str, int]) -> None:
        """Initialize a new Pizza object"""
        self.size = size
        self.toppings = toppings
        self.type = PizzaFactory().make_pizza(type, toppings)
        self.update_price()
    
    def change_size(self, new_size: str) -> None:
        """Change the size of Pizza"""
        self.size = new_size
        self.update_price()
    
    def change_topping(self, new_toppings: Dict[str, int]) -> None:
        """Change the toppings of Pizza, new toppings are passed in as a new dictionary"""
        self.toppings = new_toppings
        self.update_price()
    
    def change_type(self, new_type: str, type_recipe: Optional[Dict[str, int]]) -> None:
        """Change the type of Pizza"""
        PizzaFactory().make_pizza(type, type_recipe)
        self.update_price()

    def update_price(self) -> None:
        """Update Pizza's price"""
        self.price = size[self.size] + self.type.price
        for topping in self.toppings:
            self.price += topping_price[topping] * self.toppings[topping]
