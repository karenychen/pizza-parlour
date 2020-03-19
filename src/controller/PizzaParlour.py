from typing import Dict, List, Union
from flask import Flask, jsonify, request, abort
import os
import sys
sys.path.append("../model")

from Menu import Menu
from Order import Order

app = Flask("Assignment 2")

# === global variables ===
orders = []

# === helper functions ===
# this function check if an item is valid, an item is either a pizza or a drink
def is_valid_item(item: Union[Dict[str, str], str]) -> bool:
    if isinstance(item, str) and Menu().get_price_by_name(item) >= 0:
        return True
    elif isinstance(item, list) and len(item) == 3 and \
            isinstance(item[0], str) and isinstance(item[1], str) and isinstance(item[2], dict):
        if Menu().get_price_by_name(item[0]) < 0 or (item[1] != '' and Menu().get_price_by_name(item[1]) < 0):
            return False
        else:
            for topping in item[2]:
                if Menu().get_price_by_name(topping) < 0 or (not isinstance(item[2][topping], int)):
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
    return jsonify(Menu().get_full_menu())

# this method searches and returns the price of an item by name
@app.route('/menu/search-by-name/<name>')
def get_price_by_name(name: str):
    price = Menu().get_price_by_name(name)
    if price == -1.0:
        abort(400, 'Invalid item name.')
    else: 
        return jsonify([price])

# request.json is a list of strings and lists representing items in the order
# this method returns the order number and the total price of this order
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
    abort(400, "The order to be updated does not exist. ")

# request.json is a list of 1 element (the order number of order to be cancelled)
@app.route('/cancel-order', methods=['POST'])
def cancel_order():
    if not isinstance(request.json[0], int):
        abort(400, 'Wrong argument, expected an integer representing the order number.')
    for order in orders:
        if order.order_num == request.json[0]:
            orders.remove(order)
            return jsonify(request.json[0])
    abort(400, "The order requested to be deleted does not exist.")


if __name__ == "__main__":
    app.run(host='localhost', debug=True, port=os.environ.get('PORT', 8848))
