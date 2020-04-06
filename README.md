# Pizza Parlour

## Getting Started
Run the main Flask module by running ```python3 ./src/controller/PizzaParlour.py```
Test routes with Postman with cURL examples provided in this document on ```localhost:8848```


Run the tests by running ```coverage run --source ./src ./tests/unit_tests.py```
Check test coverage by running ```coverage report -m```

## Features
## 1. Submit a new order

### ```POST```: Route for posting a now order

#### **cURL Example: order with pizza with existing type**
``` curl
curl --location --request POST 'localhost:8848/new-order' \
--header 'Content-Type: application/json' \
--data-raw '[["small","pepperoni",{"tomato": 1, "beef": 1}], "juice"]'
```

#### **cURL Example: order with pizza with new type**
``` curl
curl --location --request POST 'localhost:8848/new-order' \
--header 'Content-Type: application/json' \
--data-raw '[["small", "", {"tomato": 1, "beef": 2}]]'
```

**Route:** ```/new-order```

**Request:** 
```json
[
    "DRINK_NAME" / 
    [
        "PIZZA_SIZE", 
        "PIZZA_TYPE", -- can be "" if user wants to create a new type
        {
            TOPPING_NAME: QUANTITY
            , ... 
        } -- an object that maps topping name to quantity
    ], ...
] -- a list of pizzas and/or drinks representing an Order model
```

**Response:**
```json
[
    ORDER_NUMBER,
    ORDER_PRICE
]
```


## 2. Update existing order
### ```POST```: Route to update an existing order

#### **cURL Example:**
``` curl
curl --location --request POST 'localhost:8848/update-order' \
--header 'Content-Type: application/json' \
--data-raw '[
	1, 
	["small","pepperoni",{"tomato": 1, "beef": 1}], 
	["large","vegetarian",{}]
]'
```

**Route:** ```/update-order```

**Request:** 

```json
[
    ORDER_NUMBER,
    "DRINK_NAME" / 
    [
        "PIZZA_SIZE", 
        "PIZZA_TYPE", 
        {
            TOPPING_NAME: QUANTITY
            , ... 
        }
    ], -- the old item to be updated
    "DRINK_NAME" / 
    [
        "PIZZA_SIZE", 
        "PIZZA_TYPE", 
        {
            TOPPING_NAME: QUANTITY
            , ... 
        }
    ] -- the new item to be updated to
]
```

**Response:**
```json
[
    ORDER_NUMBER,
    ORDER_PRICE -- the updated price
]
```

## 3. Cancel order
### ```POST```: Route to cancel an order

#### **cURL Example:**
``` curl
curl --location --request POST 'localhost:8848/cancel-order' \
--header 'Content-Type: application/json' \
--data-raw '[2]'
```

**Route:** ```/cancel-order```

**Request:**  ```[ORDER_NUMBER]```

**Response:** ```ORDER_NUMBER```

## 4. Ask for pickup or delivery
### ```POST```: Route to set an order as pickup

#### **cURL Example:**
```curl
curl --location --request POST 'localhost:8848/add-pickup' \
--header 'Content-Type: application/json' \
--data-raw '[1]'
```

**Route:** ```/add-pickup```

**Request:**  ```[ORDER_NUMBER]```

**Response:** ```ORDER_NUMBER```

### ```POST```: Route to set an order as in-house delivery

#### **cURL Example:**
```curl
curl --location --request POST 'localhost:8848/add-in-house-delivery' \
--header 'Content-Type: application/json' \
--data-raw '[3, "Call me when arriving the lobby", "253 College Street"]'
```

**Route:** ```/add-in-house-delivery```

**Request:** 
```json
[
    ORDER_NUMBER, 
    ORDER_DETAILS, -- some words
    ORDER_ADDRESS, -- some words
]
```

**Response:** ```ORDER_NUMBER```

### ```POST```: Route to set an order as ubereats delivery

#### **cURL Example:**
``` curl
curl --location --request POST 'localhost:8848/add-uber-eats' \
--header 'Content-Type: application/json' \
--data-raw '[4, "Call me when arriving the lobby", "253 College Street"]'
```

**Route:** ```/add-uber-eats```

**Request:** 
```json
[
    ORDER_NUMBER, 
    ORDER_DETAILS, -- some words
    ORDER_ADDRESS, -- some words
]
```

**Response:** ```ORDER_NUMBER```

### ```GET```: Route to set an order as foodora delivery

#### **cURL Example:**
``` curl
curl --location --request GET 'localhost:8848/add-foodora'
```

**Route:** ```/add-foodora```

**Request:** does not have a body, reads from the first line in ```./data/foodora.csv```

**Response:** ```ORDER_NUMBER```

## 5. Ask for the menu
### ```GET```: Route for getting the full menu

#### **cURL Example:** 
```curl
curl --location --request GET 'localhost:8848/menu/full'
```

**Route:** ```/menu/full```

**Request:** does not have a body

**Response:**
```json
{
  "drinks": {
    "coke": 1.5,
    "coke-zero": 1.5,
    "diet-coke": 1.5,
    "diet-pepsi": 1.5,
    "dr.pepper": 1.5,
    "juice": 2.0,
    "pepsi": 1.5,
    "water": 1.0
  },
  "pizza-size": {
    "large": 10.0,
    "medium": 8.0,
    "small": 6.0,
    "xlarge": 12.0
  },
  "pizza-topping": {
    "beef": 4.0,
    "chicken": 2.0,
    "jalapeno": 1.0,
    "mushroom": 1.0,
    "olive": 1.0,
    "pepperoni": 3.0,
    "tomato": 1.0
  },
  "pizza-type": {
    "margherita": 7.0,
    "neapolitan": 15.0,
    "pepperoni": 13.0,
    "vegetarian": 7.0
  }
}
```

### ```GET```: Route for getting the price of a single item by name
#### **cURL Example:** 
```curl
curl --location --request GET 'localhost:8848/menu/search-by-name/diet-coke'
```

**Route:** ```/menu/search-by-name/<item-name>```

**Request:** does not have a body

**Response:** ```SOME_NUMBER```

## Design Patterns
### In this assignment, we implemented our features with the following design patterns:

### Factory Design Pattern
We implemented the factory design pattern in the delivery feature in our application. We used a DeliveryFactory class to create subclass instances of the Delivery class based on different delivery types.

The reason why we chose to use the Factory Design pattern was because it removes instantiation of actual implementation classes from the client code. Factory pattern makes our code more robust, less coupled and easier to extend. 


### (Potential) MVC Design Pattern
We divided our product into Model and Controller. Model contains application data such as Menu class and Order class. Controller includes server calls to execute appropriate action to events. There isn't a View component so far since we are only developing the backend for our application, but the View could be potentially developed in the future.

The reason why we choose to use MVC design pattern was because it is easier to maintain the application due to the separation of concern. MVC also supports rapid and parallel development which leads to a more efficient process. 

## Pair Programming
### Process
We first designed the the whole project structure together, then implemented features with pair programming. Due to the COVID-19 situation, we have been pair programming via TeamViewer.

### The following features are pair programmed:
#### 1. Menu Viewing & Submitting New Orders
**Driver**: Karen Chen
**Navigator**: Kexin Lin

#### 2. Asking for Pickup / Delivery
**Driver**: Kexin Lin
**Navigator**: Karen Chen

### Reflection
Our pair programming process went very smoothly overall. Since we designed the overall structure before we started coding, we are both clear on features we need to implement and how we are going to implement them. And as the navigator is also watching while the driver is coding, both of us are familiar with not only the parts we wrote ourselves but, also the parts the other person wrote.

One thing we liked about the process was that we were writing higher quality codes and making less mistakes compared to when we were developing features individually. 

One thing we disliked about the process was that we had to perform this process online instead of in person, it is less efficient since we are not physically beside each other. 

## Code Craftsmanship
- We used **Python Linter** in VS Code to highlight syntactical and stylistic problems in our source code.
- We also used **Python type annotation** throughout our development process to help us document our code and potentially catch certain errrors. 