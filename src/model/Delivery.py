from typing import List, Dict, Union, Optional
import os
import sys
import csv

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
foodora_file = os.path.join(THIS_FOLDER, './../../data/foodora.csv')

class DeliveryFactory:
    '''A factory to generate object of Delivery class based on given type.'''
    def create_valid_delivery(self, delivery_type: int, input: list):
        '''Check whether the input is invalid. If so, initializes a new Delivery in the pizza parlour 
        and return (0, Delivery), else return (error_code, error_message).'''
        if(delivery_type == 0):  # type 0 means an in-house delivery
            # check if the input is valid before initiating an in-house delivery
            if len(input) != 3:
                return (400, 'Wrong number of arguments, expected 3.')
            elif not isinstance(input[0], int):
                return (400, 'Invalid order number.')
            elif not isinstance(input[1], str):
                return (400, 'Invalid order details.')
            elif not isinstance(input[2], str):
                return (400, 'Invalid address.')
            return (0, InHouseDelivery(input[0], input[1], input[2]))

        if(delivery_type == 1):  # type 1 means a Uber Eats delivery
            # check if the input is valid before initiating a Uber Eats delivery
            if len(input) != 3:
                return (400, 'Wrong number of arguments, expected 3.')
            elif not isinstance(input[0], int):
                return (400, 'Invalid order number.')
            elif not isinstance(input[1], str):
                return (400, 'Invalid order details.')
            elif not isinstance(input[2], str):
                return (400, 'Invalid address.')
            return (0, UberEatsDelivery(input[0], input[1], input[2]))

        if(delivery_type == 2):  # type 2 means a Foodora delivery
            # check if the input is valid before initiating a Foodora delivery
            with open(foodora_file, 'r') as f:
                reader = csv.reader(f)
                result = list(reader)[0]
            if len(result) != 3:
                return (400, 'Wrong number of arguments in the first line of the csv file, expected 3.')
            elif not result[0].isdigit():
                return (400, 'Invalid order number.')
            return (0, FoodoraDelivery(int(result[0]), result[1], result[2]))


class Delivery:
    '''A food delivery request for orders in the pizza parlour.
    
    === Attributes ===
    order_num: the number of the order requested for delivery
    order_details: the details added for the order requested for delivery
    address: the address for the the order requested for delivery
    '''

    order_num: int
    order_details: str
    address: str

    def __init__(self, order_num, order_details, address) -> None:
        self.order_num = order_num
        self.order_details = order_details
        self.address = address

    

class InHouseDelivery(Delivery):
    '''An in-house delivery request for orders in the pizza parlour.
    Class leave for further extension.'''
    pass


class UberEatsDelivery(Delivery):
    '''A Uber Eats delivery request for orders in the pizza parlour.
    Class leave for further extension.'''
    pass


class FoodoraDelivery(Delivery):
    '''A Foodora delivery request for orders in the pizza parlour.
    Class leave for further extension.'''
    pass