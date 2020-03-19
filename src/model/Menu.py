from typing import Dict
import json
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
menu_file = os.path.join(THIS_FOLDER, './../../data/menu.json')

# load topping prices
with open(menu_file) as f:
    menu = json.load(f)

class Menu:
    '''A menu in the pizza parlour.

    === Attribute ===
    menu: a nested dictionary implementing the full menu
    '''
    menu: Dict[str, Dict[str, int]]

    def __init__(self):
        '''Initialize a new Menu object.'''
        self.menu =  menu

    def get_full_menu(self) -> Dict[str, Dict[str, int]]:
        '''Get the full menu in pizza parlour. '''
        return self.menu

    def get_price_by_name(self, name: str) -> float:
        '''Get the price of a specific item in the menu by name.
        Precondition: name is a key in the inner dictionaries.
        '''
        for category in menu:
            if name in menu[category]:
                return menu[category][name]
        return -1.0

    



