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
        if(old_item in self.items):
            self.items.remove(old_item)
        self.items.append(new_item)
        self.update_price()

