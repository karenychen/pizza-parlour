from typing import List, Dict, Union, Optional
from Menu import Menu

counter = 1

class Order:
    '''An order in the pizza parlour.
    
    === Attributes ===
    order_num: the order number of this order
    items: a list of dictionaries contained in this order
    price: the total price of this order
    '''
    order_num: int
    items: List[Union[Dict[str, str], str]]
    price: float

    def __init__(self, items: List[Union[Dict[str, str], str]]) -> None:
        '''Initializes a new Order in the pizza parlour.'''
        global counter
        self.order_num = counter
        counter += 1
        self.items = items
        self.update_price()
    
    def update_price(self) -> None:
        menu = Menu()
        self.price = 0
        for item in self.items:
            if isinstance(item, str): # item is a drink
                self.price += menu.get_price_by_name(item)
            else: # item is a pizza
                self.price += menu.get_price_by_name(item[0])
                if item[1] != '':
                    self.price += menu.get_price_by_name(item[1])
                for topping in item[2]:
                    self.price += menu.get_price_by_name(topping) * item[2][topping]
    
    def replace_item(self, old_item: Union[Dict[str, str], str], new_item: Union[Dict[str, str], str]) -> None:
        self.items.remove(old_item)
        self.items.append(new_item)
        self.update_price()


# class Order:
#     """An order in the pizza parlour.

#     === Attributes ===
#     order_num: the order number of this order
#     items: a list of items contained in this order
#     price: the total price of this order
#     method: can either be "pickup", "delivery", "ubereats" or "foodora"
#     """
#     order_num: int
#     items: List[Union[Pizza, Drink]]
#     price: float
#     method: str

#     def __init__(self, items: List[Union[Pizza, Drink]], method: str) -> None:
#         """Initialize a new Order object."""
#         global counter
#         self.order_num = counter
#         counter += 1
#         self.items = items
#         self.update_price()
#         self.method = method
    
#     def add_pizza(self, size: str, type: str, toppings: Dict[str, int], type_recipe: Optional[Dict[str, int]]) -> bool:
#         """Add a new Pizza to the Order Returns false if addition is successful."""
#         pizza = Pizza(size, type, toppings)
#         self.items.append(pizza)
#         self.update_price()
#         return True
    
#     def add_drink(self, name: str) -> bool:
#         """Add a new Drink to the Order. Returns true if addition is successful."""
#         self.items.append(Drink(name))
#         self.update_price()
#         return True
        
#     def delete_item(self, index: int) -> Union[Pizza, Drink]:
#         """Delete an item in the Order given its index in the list, returns the deleted item.
#         Precondition: index < len(self.items)
#         """
#         deleted = self.items.pop(index)
#         self.update_price()
#         return deleted

#     def update_price(self) -> None:
#         """Updates the total price of this Order."""
#         self.price = 0
#         for item in self.items:
#             self.price += item.price
