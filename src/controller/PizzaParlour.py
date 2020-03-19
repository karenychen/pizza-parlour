from flask import Flask, jsonify, request, abort
import os
import sys
sys.path.append("../model")

from Menu import Menu
from Order import Order

app = Flask("Assignment 2")

# global variables
orders = []

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
    return jsonify([Menu().get_price_by_name(name)])

# request.json is a list of strings and lists representing items in the order
# this method returns the order number and the total price of this order
@app.route('/new-order', methods=['POST'])
def new_order():
    items = request.json
    order = Order(items)
    orders.append(order)
    return jsonify([order.order_num, order.price])

# request.json is a list of 3 elements where the first element is the order number
# second element is the old item (unedited), third element is the new item (edited).
# this method returns the order number and the updated total price of this order
@app.route('/update-order', methods=['POST'])
def update_order():
    order = orders[request.json[0] - 1]
    old_item = request.json[1]
    new_item = request.json[2]
    order.replace_item(old_item, new_item)
    print(len(orders))
    return jsonify([order.order_num, order.price])

if __name__ == "__main__":
    app.run(host='localhost', debug=True, port=os.environ.get('PORT', 8848))
