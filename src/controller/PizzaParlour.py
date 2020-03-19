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

@app.route('/menu/full')
def get_full_menu():
    return jsonify(Menu().get_full_menu())

@app.route('/menu/search-by-name/<name>')
def get_price_by_name(name):
    return jsonify([Menu().get_price_by_name(name)])

if __name__ == "__main__":
    app.run(host='localhost', debug=True, port=os.environ.get('PORT', 8848))
