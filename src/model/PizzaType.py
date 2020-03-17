from typing import Dict, List, Optional

import json
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
recipe_file = os.path.join(THIS_FOLDER, './../../data/pizza_recipe.json')

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
topping_file = os.path.join(THIS_FOLDER, './../../data/topping_price.json')

# load recipes
with open(recipe_file) as f:
    recipe = json.load(f)

# load topping prices
with open(topping_file) as f:
    topping_price = json.load(f)


def get_recipe(pizza_type):
    return recipe[pizza_type]


def calculate_price(recipe: Dict[str, int]):
    total_price = 0
    for item in recipe:
        item_num = recipe[item]
        total_price += topping_price[item] * item_num
    return total_price


class PizzaType:
    name: str
    recipe: Dict[str, int]
    price: float

    def __init__(self, name: str, recipe: Dict[str, int], price: float):
        self.name = name
        self.recipe = recipe
        self.price = price

    def get_price(self):
        raise NotImplementedError


class Pepperoni(PizzaType):
    def __init__(self):
        super().__init__("pepperoni", recipe["pepperoni"],
                         calculate_price(recipe["pepperoni"]))

    def get_price(self):
        return self.price


class Margherita(PizzaType):
    def __init__(self):
        super().__init__("margherita", recipe["margherita"],
                         calculate_price(recipe["margherita"]))

    def get_price(self):
        return self.price


class Vegetarian(PizzaType):
    def __init__(self):
        super().__init__("vegetarian", recipe["vegetarian"],
                         calculate_price(recipe["vegetarian"]))

    def get_price(self):
        return self.price


class Neapolitan(PizzaType):
    def __init__(self):
        super().__init__("neapolitan", recipe["neapolitan"],
                         calculate_price(recipe["neapolitan"]))

    def get_price(self):
        return self.price


class MakeYourOwn(PizzaType):
    def __init__(self, recipe: Dict[str, int]):
        super().__init__("make your own", recipe, calculate_price(recipe))

    def get_price(self):
        return self.price


class PizzaFactory:
    def make_pizza(self, pizza_type: str, recipe: Optional[Dict[str, int]]):
        if(pizza_type == "pepperoni"):
            return Pepperoni()
        if(pizza_type == "margherita"):
            return Margherita()
        if(pizza_type == "vegetarian"):
            return Vegetarian()
        if(pizza_type == "neapolitan"):
            return Neapolitan()
        if(pizza_type == "make your own"):
            return MakeYourOwn(recipe)
