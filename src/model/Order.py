from typing import List, Union
from Pizza import Pizza
from Drink import Drink

counter = 0

class Order:
    """An order in the pizza parlour.

    === Attributes ===
    order_num: the order number of this order
    items: a list of items contained in this order
    price: the total price of this order
    method: can either be "pickup", "delivery", "ubereats" or "foodora"
    """
    order_num: int
    items: List[Union[Pizza, Drink]]
    price: float
    method: str

    def __init__(self, items: List[Union[Pizza, Drink]], price: float, method: str) -> None:
        self.order_num = counter
        counter += 1
        self.items = items
        self.price = update_price()
        self.method = method
    
    def add_pizza(self, size: str, type: str, toppings: Dict[str, int], type_recipe: Optional[Dict[str, int]]) -> bool:
        if type == 'pepperoni' or type == 'margherita' or type == 'vegetarian' or type == 'neapolitan':
            pizza = Pizza(size, type, toppings)
        else: 
            pizza = Pizza(size, type, toppings, type_recipe)
        self.items.append(pizza)
        self.update_price()
        return True
    
    def add_drink(self, name: str) -> bool:
        self.items.append(Drink(name))
        self.update_price()
        return True
        
    def delete_item(self, index: int) -> Union[Pizza, Drink]:
        """Precondition: index < len(self.items)"""
        deleted = self.items.pop(index)
        self.update_price()
        return deleted

    def update_price(self) -> None:
        self.price = 0
        for item in items:
            self.price += item.price
    

            

