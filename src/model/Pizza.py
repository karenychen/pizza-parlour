from typing import Dict, List, Optional

class Pizza:
    """ A Pizza class.

    === Attributes ===
    size: Size of the pizza, can be either "small", "medium", "large" or "xlarge"
    type: type of the pizza
    toppings: a dictionary with all the additional toppings
    price: price of the pizza
    """
    size: str
    type: PizzaType
    toppings: Dict[str, int]
    price: float
    
    def __init__(self, size: str, type: str, toppings: Dict[str, int], type_recipe: Optional[Dict[str, int]]) -> None:
        self.size = size
        self.toppings = toppings
        if type == 'pepperoni' or type == 'margherita' or type == 'vegetarian' or type == 'neapolitan':
            pass
        else:
            pass
        self.update_price()
    
    def change_size(self, new_size: str) -> None:
        self.size = new_size
        self.update_price()
    
    def change_topping(self, new_toppings: Dict[str, int]) -> None:
        self.toppings = new_toppings
        self.update_price()
    
    def change_type(self, new_type: str) -> None:
        if type == 'pepperoni' or type == 'margherita' or type == 'vegetarian' or type == 'neapolitan':
            pass
        else:
            pass
        self.update_price()

    def update_price(self) -> None:
        pass
