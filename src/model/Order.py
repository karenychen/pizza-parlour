from typing import List, Dict, Union, Optional
from Pizza import Pizza
from Drink import Drink

counter = 1

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

    def __init__(self, items: List[Union[Pizza, Drink]], method: str) -> None:
        """Initialize a new Order object."""
        global counter
        self.order_num = counter
        counter += 1
        self.items = items
        self.update_price()
        self.method = method
    
    def add_pizza(self, size: str, type: str, toppings: Dict[str, int], type_recipe: Optional[Dict[str, int]]) -> bool:
        """Add a new Pizza to the Order Returns false if addition is successful."""
        pizza = Pizza(size, type, toppings)
        self.items.append(pizza)
        self.update_price()
        return True
    
    def add_drink(self, name: str) -> bool:
        """Add a new Drink to the Order. Returns true if addition is successful."""
        self.items.append(Drink(name))
        self.update_price()
        return True
        
    def delete_item(self, index: int) -> Union[Pizza, Drink]:
        """Delete an item in the Order given its index in the list, returns the deleted item.
        Precondition: index < len(self.items)
        """
        deleted = self.items.pop(index)
        self.update_price()
        return deleted

    def update_price(self) -> None:
        """Updates the total price of this Order."""
        self.price = 0
        for item in self.items:
            self.price += item.price
