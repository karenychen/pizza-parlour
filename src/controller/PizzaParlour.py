from typing import Dict, List, Union
from flask import Flask, jsonify, request, abort
import os
import sys
import csv

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
model_folder = os.path.join(THIS_FOLDER, '../model')
sys.path.append(model_folder)
foodora_file = os.path.join(THIS_FOLDER, './../../data/foodora.csv')

from Menu import Menu
from Order import Order

app = Flask("Assignment 2")

# === global variables ===
menu_service = Menu()
orders = []  # List[Union[List[str, str, Dict[str, int]], str]]

pickup_orders = []  # List[int], list of order numbers
in_house_delivery = []  # list of list with order number, order details, address as the three elements inside
uber_eats_delivery = []  # list of list with order number, order details, address as the three elements inside
foodora_delivery = []  # list of list with order number, order details, address as the three elements inside

# === helper functions ===
# this function check if an item is valid, an item is either a pizza or a drink
# example valid input can be "diet-coke" or ["small", "margherita", {"olive": 2, "beef": 1}]
def is_valid_item(item: Union[List[Union[str, str, Dict[str, int]]], str]) -> bool:
    if isinstance(item, str) and menu_service.get_price_by_name(item) >= 0:
        return True
    elif isinstance(item, list) and len(item) == 3 and \
            isinstance(item[0], str) and isinstance(item[1], str) and isinstance(item[2], dict):
        if menu_service.get_price_by_name(item[0]) < 0 or (item[1] != '' and menu_service.get_price_by_name(item[1]) < 0):
            return False
        else:
            for topping in item[2]:
                if menu_service.get_price_by_name(topping) < 0 or (not isinstance(item[2][topping], int)):
                    return False
            return True
    else: 
        return False

# this function checks if an order is valid. An order is valid if all of its items are.
def is_valid_order(items: List[Union[Dict[str, str], str]]) -> bool:
    for item in items:
        if not is_valid_item(item):
            return False
    return True

@app.route('/pizza')
def welcome_pizza():
    return 'Welcome to Pizza Planet!'

# this method returns the full menu in the pizza parlour
@app.route('/menu/full')
def get_full_menu():
    return jsonify(menu_service.get_full_menu())

# this method searches and returns the price of an item by name
@app.route('/menu/search-by-name/<name>')
def get_price_by_name(name: str):
    price = menu_service.get_price_by_name(name)
    if price < 0:
        abort(404, 'The item name does not exist.')
    else: 
        return jsonify([price])

# request.json is a list of strings and lists representing items in the order
# this method returns the order number and the total price of this order
# Example of request.json: ["diet-coke", ["small", "margherita", {"olive": 2, "beef": 1}]]
@app.route('/new-order', methods=['POST'])
def new_order():
    items = request.json
    if is_valid_order(items):
        order = Order(items)
        orders.append(order)
        return jsonify([order.order_num, order.price])
    else:
        abort(400, 'Invalid order details.')

# request.json is a list of 3 elements where the first element is the order number
# second element is the old item (unedited), third element is the new item (edited).
# this method returns the order number and the updated total price of this order
# note that update_order would only update 1 item if there are multiple identical items.
@app.route('/update-order', methods=['POST'])
def update_order():
    if len(request.json) != 3:
        abort(400, 'Wrong number of arguments, expected 3.')
    elif not isinstance(request.json[0], int):
        abort(400, 'Invalid order number.')
    elif not (is_valid_order(request.json[1:])):
        abort(400, 'Invalid order item(s).')
    for order in orders:
        if order.order_num == request.json[0]:
            old_item = request.json[1]
            new_item = request.json[2]
            order.replace_item(old_item, new_item)
            return jsonify([order.order_num, order.price])
    abort(404, "The order to be updated does not exist. ")

# request.json is a list of 1 element (the order number of order to be cancelled)
@app.route('/cancel-order', methods=['POST'])
def cancel_order():
    if not isinstance(request.json[0], int):
        abort(400, 'Wrong argument, expected an integer representing the order number.')
    for order in orders:
        if order.order_num == request.json[0]:
            orders.remove(order)
            return jsonify(request.json[0])
    abort(404, "The order requested to be deleted does not exist.")

# request.json is a list of 1 element (the order number of order for pickup)
@app.route('/add-pickup', methods=['POST'])
def add_pickup():
    if not isinstance(request.json[0], int):
        abort(400, 'Wrong argument, expected an integer representing the order number.')
    # check if the order has already been added to the pickup list
    for pickup_order in pickup_orders:
        if pickup_order[0] == request.json[0]:
            abort(400, "The order has already been added for pickup.")

    # check if the order number exists.
    for order in orders:
        if order.order_num == request.json[0]:
            pickup_orders.append(request.json[0])
            return jsonify(request.json[0])
    abort(404, "The order number requested for pickup does not exist.")

# request.json is a list of 3 element: [order_number: int, order_details: str, address: str]
# Example of request.json: [56, "Call me when arriving the lobby", "253 College Street"]
@app.route('/add-in-house-delivery', methods=['POST'])
def add_in_house_delivery():
    if len(request.json) != 3:
        abort(400, 'Wrong number of arguments, expected 3.')
    elif not isinstance(request.json[0], int):
        abort(400, 'Invalid order number.')
    elif not isinstance(request.json[1], str):
        abort(400, 'Invalid order details.')
    elif not isinstance(request.json[2], str):
        abort(400, 'Invalid address.')
    
    # check if the order has already been added to the in-house delivery list.
    for delivery in in_house_delivery:
        if delivery[0] == request.json[0]:
            abort(400, "The order has already been added for in-house delivery.")

    # check if the order number exists.
    for order in orders:
        if order.order_num == request.json[0]:
            new_delivery = [request.json[0], request.json[1], request.json[2]]
            in_house_delivery.append(new_delivery)
            return jsonify(request.json[0])
    abort(404, "The order number for in-house delivery does not exist. ")

# request.json is a list of 3 element: [order_number: int, order_details: str, address: str]
# Example of request.json: [56, "Call me when arriving the lobby", "253 College Street"]
@app.route('/add-uber-eats', methods=['POST'])
def add_uber_eats():
    if len(request.json) != 3:
        abort(400, 'Wrong number of arguments, expected 3.')
    elif not isinstance(request.json[0], int):
        abort(400, 'Invalid order number.')
    elif not isinstance(request.json[1], str):
        abort(400, 'Invalid order details.')
    elif not isinstance(request.json[2], str):
        abort(400, 'Invalid address.')

    # check if the order has already been added to the in-house delivery list.
    for delivery in uber_eats_delivery:
        if delivery[0] == request.json[0]:
            abort(400, "The order has already been added for Uber Eats delivery.")
    
    # check if the order number exists.
    for order in orders:
        if order.order_num == request.json[0]:
            new_uber_eats = [request.json[0], request.json[1], request.json[2]]
            uber_eats_delivery.append(new_uber_eats)
            return jsonify(request.json[0])
    abort(404, "The order number for Uber Eats delivery does not exist. ")

# Read the first line in foodora.csv, and add that order information into foodora_delivery list after checking
# if the order has been added yet.
@app.route('/add-foodora')
def add_foodora():
    with open(foodora_file, 'r') as f:
        reader = csv.reader(f)
        result = list(reader)[0]
    
    if len(result) != 3:
        abort(400, 'Wrong number of arguments in the first line of the csv file, expected 3.')
    elif not result[0].isdigit():
        abort(400, 'Invalid order number.')
    
    order_num = result[0]
    # check if the order has already been added to the Foodora delivery list.
    for delivery in foodora_delivery:
        if delivery[0] == order_num:
            abort(400, "The order has already been added for in-house delivery.")

    # check if the order number exists.
    for order in orders:
        if order.order_num == order_num:
            new_foodora = [order_num, request.json[1], request.json[2]]
            uber_eats_delivery.append(new_foodora)
            return jsonify(order_num)
    abort(404, "The order number for Foodora delivery does not exist. ")



if __name__ == "__main__":
    app.run(host='localhost', debug=True, port=os.environ.get('PORT', 8848))
