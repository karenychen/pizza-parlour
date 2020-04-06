import os, sys, json
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
app_folder = os.path.join(THIS_FOLDER, '../src/controller')
sys.path.append(app_folder)

import PizzaParlour
from PizzaParlour import app
import unittest

class AppTestCase(unittest.TestCase):

    def test_01_is_valid_item(self):
        valid_item1 = "diet-coke"
        valid_item2 = ["small", "margherita", {"olive": 2, "beef": 1}]
        self.assertTrue(PizzaParlour.is_valid_item(valid_item1))
        self.assertTrue(PizzaParlour.is_valid_item(valid_item2))

        invalid_item1 = "lalala"
        invalid_item2 = ["verysmall", "margherita", {"olive": 2, "beef": 1}]
        invalid_item3 = ["small", "margherita", {"olive": "two", "beef": 1}]
        invalid_item4 = ["small", "margheritaaaa", {"olive": "two", "beef": 1}]
        self.assertFalse(PizzaParlour.is_valid_item(invalid_item1))
        self.assertFalse(PizzaParlour.is_valid_item(invalid_item2))
        self.assertFalse(PizzaParlour.is_valid_item(invalid_item3))
        self.assertFalse(PizzaParlour.is_valid_item(invalid_item4))

    def test_02_is_valid_order(self):
        valid_order1 = ["diet-coke"]
        valid_order2 = [["small", "margherita", {"olive": 2, "beef": 1}]]
        valid_order3 = ["diet-coke", ["small", "margherita", {"olive": 2, "beef": 1}]]
        self.assertTrue(PizzaParlour.is_valid_order(valid_order1))
        self.assertTrue(PizzaParlour.is_valid_order(valid_order2))
        self.assertTrue(PizzaParlour.is_valid_order(valid_order3))

        invalid_order1 = ["lalala"]
        invalid_order2 = ["diet-coke", ["verysmall", "margherita", {"olive": 2, "beef": 1}]]
        invalid_order3 = ["diet-coke", ["small", "margheritaaa", {"olive": 2, "beef": 1}]]
        self.assertFalse(PizzaParlour.is_valid_order(invalid_order1))
        self.assertFalse(PizzaParlour.is_valid_order(invalid_order2))
        self.assertFalse(PizzaParlour.is_valid_order(invalid_order3))

    def test_03_pizza(self):
        response = app.test_client().get('/pizza')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Welcome to Pizza Planet!')

    
    def test_04_menu_full(self):
        response = app.test_client().get('/menu/full')
        self.assertEqual(response.status_code, 200)
        json_reponse = json.loads(response.get_data(as_text=True))
        self.assertEqual(set(json_reponse.keys()), set(["pizza-size", "pizza-type", "pizza-topping", "drinks"]))

    def test_05_menu_search_by_name(self):
        response1 = app.test_client().get('/menu/search-by-name/margherita')
        self.assertEqual(response1.status_code, 200)
        json_reponse1 = json.loads(response1.get_data(as_text=True))
        self.assertEqual(json_reponse1, 7.00)

        response2 = app.test_client().get('/menu/search-by-name/margheritaaaa')
        self.assertEqual(response2.status_code, 404)

    def test_06_new_order(self):
        with app.test_client() as client:
            # send data as POST form to endpoint
            sent = ["diet-coke", ["small", "margherita", {"olive": 2, "beef": 1}]]
            result = client.post(
                '/new-order',
                json=sent
            )
            # check result from server with expected data
            self.assertEqual(
                json.loads(result.data),
                [1, 20.5])

            # send data as POST form to endpoint
            sent = ["pepsi"]
            result = client.post(
                '/new-order',
                json=sent
            )
            # check result from server with expected data
            self.assertEqual(
                json.loads(result.data),
                [2, 1.50])

            # send invalid data as POST form to endpoint
            sent = ["lalala"]
            result = client.post(
                '/new-order',
                json=sent
            )
            # check result from server with invalid data
            self.assertEqual(result.status_code, 400)

    def test_07_update_order(self):
        with app.test_client() as client:
            # test 1, send valid data as POST form to endpoint
            sent = [1, ["small", "margherita", {"olive": 2, "beef": 1}], ["large", "margherita", {"olive": 2}]]
            result = client.post(
                '/update-order',
                json=sent
            )
            # check result from server with expected data
            self.assertEqual(
                json.loads(result.data),
                [1, 20.5])

            # test 2, send invalid data (absense of order number)
            sent = [["small", "margherita", {"olive": 2, "beef": 1}], ["large", "margherita", {"olive": 2}]]
            result = client.post(
                '/update-order',
                json=sent
            )
            # check result from server with invalid data
            self.assertEqual(result.status_code, 400)

            # test 3, send invalid data (invalid form of order number)
            sent = ["hello", ["small", "margherita", {"olive": 2, "beef": 1}], ["large", "margherita", {"olive": 2}]]
            result = client.post(
                '/update-order',
                json=sent
            )
            # check result from server with invalid data
            self.assertEqual(result.status_code, 400)

            # test 4, send invalid data (invalid order)
            sent = [1, ["verysmall", "margheritaa", {"olive": 2, "beef": 1}], ["large", "margherita", {"olive": 2}]]
            result = client.post(
                '/update-order',
                json=sent
            )
            # check result from server with invalid data
            self.assertEqual(result.status_code, 400)

            # test 5, send invalid data (order number does not exist)
            sent = [-99, ["small", "margherita", {"olive": 2, "beef": 1}], ["large", "margherita", {"olive": 2}]]
            result = client.post(
                '/update-order',
                json=sent
            )
            # check result from server with invalid data
            self.assertEqual(result.status_code, 404)


    def test_08_cancel_order(self):
        with app.test_client() as client:
            # test 1, send valid data as POST
            sent = [2]
            result = client.post(
                '/cancel-order',
                json=sent
            )
            # check result from server with expected data
            self.assertEqual(
                json.loads(result.data), 2)

            # send invalid data as POST form to endpoint
            sent = ["invalid stuff"]
            result = client.post(
                '/cancel-order',
                json=sent
            )
            # check result from server with invalid data
            self.assertEqual(result.status_code, 400)

            # send invalid data as POST form to endpoint
            sent = [-99]
            result = client.post(
                '/cancel-order',
                json=sent
            )
            # check result from server with invalid data
            self.assertEqual(result.status_code, 404)

    def test_09_add_pickup(self):
        with app.test_client() as client:
            # send valid data as POST form to endpoint
            sent = [1]
            result = client.post(
                '/add-pickup',
                json=sent
            )
            # check result from server with expected data
            self.assertEqual(
                json.loads(result.data), 1)

            # send invalid data as POST form to endpoint (already added to pickup or delivery)
            sent = [1]
            result = client.post(
                '/add-pickup',
                json=sent
            )
            # check result from server with invalid data
            self.assertEqual(result.status_code, 400)

            # send invalid data as POST form to endpoint
            sent = ["lalala"]
            result = client.post(
                '/add-pickup',
                json=sent
            )
            # check result from server with invalid data
            self.assertEqual(result.status_code, 400)

            # send invalid data as POST form to endpoint
            sent = [-99]
            result = client.post(
                '/add-pickup',
                json=sent
            )
            # check result from server with invalid data
            self.assertEqual(result.status_code, 404)

    def test_10_add_in_house_delivery(self):
        with app.test_client() as client:
            # create a new order (order number is 3)
            sent = ["diet-coke", ["small", "margherita", {"olive": 2, "beef": 1}]]
            result = client.post(
                '/new-order',
                json=sent
            )

            # send valid data as POST form to endpoint
            sent = [3, "Call me when arriving the lobby", "253 College Street"]
            result = client.post(
                '/add-in-house-delivery',
                json=sent
            )
            # check result from server with expected data
            self.assertEqual(
                json.loads(result.data), 3)

            # send invalid data as POST form to endpoint (already added to pickup or delivery)
            sent = [1, "Call me when arriving the lobby", "253 College Street"]
            result = client.post(
                '/add-in-house-delivery',
                json=sent
            )
            # check result from server with invalid data
            self.assertEqual(result.status_code, 400)

            # send invalid data as POST form to endpoint
            sent = ["lalala"]
            result = client.post(
                '/add-in-house-delivery',
                json=sent
            )
            # check result from server with invalid data
            self.assertEqual(result.status_code, 400)

            # send invalid data as POST form to endpoint
            sent = [3, 1, "253 College Street"]
            result = client.post(
                '/add-in-house-delivery',
                json=sent
            )
            # check result from server with invalid data
            self.assertEqual(result.status_code, 400)

            # send invalid data as POST form to endpoint
            sent = ["hello", "Call me when arriving the lobby", "253 College Street"]
            result = client.post(
                '/add-in-house-delivery',
                json=sent
            )
            # check result from server with invalid data
            self.assertEqual(result.status_code, 400)

            # send invalid data as POST form to endpoint
            sent = [1, "Call me when arriving the lobby", 1]
            result = client.post(
                '/add-in-house-delivery',
                json=sent
            )
            # check result from server with invalid data
            self.assertEqual(result.status_code, 400)

            # send invalid data as POST form to endpoint
            sent = [-99, "Call me when arriving the lobby", "253 College Street"]
            result = client.post(
                '/add-in-house-delivery',
                json=sent
            )
            # check result from server with invalid data
            self.assertEqual(result.status_code, 404)


    def test_11_add_uber_eats(self):
        with app.test_client() as client:
            # create a new order (order number is 4)
            sent = ["diet-coke", ["small", "margherita", {"olive": 2, "beef": 1}]]
            result = client.post(
                '/new-order',
                json=sent
            )

            # send valid data as POST form to endpoint
            sent = [4, "Call me when arriving the lobby", "253 College Street"]
            result = client.post(
                '/add-uber-eats',
                json=sent
            )
            # check result from server with expected data
            self.assertEqual(
                json.loads(result.data), 4)

            # send invalid data as POST form to endpoint (already added to pickup or delivery)
            sent = [1, "Call me when arriving the lobby", "253 College Street"]
            result = client.post(
                '/add-uber-eats',
                json=sent
            )
            # check result from server with invalid data
            self.assertEqual(result.status_code, 400)

            # send invalid data as POST form to endpoint
            sent = ["lalala"]
            result = client.post(
                '/add-uber-eats',
                json=sent
            )
            # check result from server with invalid data
            self.assertEqual(result.status_code, 400)

            # send invalid data as POST form to endpoint
            sent = [1, 1, "253 College Street"]
            result = client.post(
                '/add-uber-eats',
                json=sent
            )
            # check result from server with invalid data
            self.assertEqual(result.status_code, 400)

            # send invalid data as POST form to endpoint
            sent = ["hello", "Call me when arriving the lobby", "253 College Street"]
            result = client.post(
                '/add-uber-eats',
                json=sent
            )
            # check result from server with invalid data
            self.assertEqual(result.status_code, 400)

            # send invalid data as POST form to endpoint (already added to pickup or delivery)
            sent = [1, "Call me when arriving the lobby", 1]
            result = client.post(
                '/add-uber-eats',
                json=sent
            )
            # check result from server with invalid data
            self.assertEqual(result.status_code, 400)

            # send invalid data as POST form to endpoint
            sent = [-99, "Call me when arriving the lobby", "253 College Street"]
            result = client.post(
                '/add-uber-eats',
                json=sent
            )
            # check result from server with invalid data
            self.assertEqual(result.status_code, 404)

    def test_12_add_foodora(self):
        with app.test_client() as client:
            # create a new order (order number is 5)
            sent = ["diet-coke", ["small", "margherita", {"olive": 2, "beef": 1}]]
            client.post('/new-order',json=sent)

        # send valid data as POST form to endpoint
        response = app.test_client().get('/add-foodora')
        # check result from server with expected data
        self.assertEqual(json.loads(response.data), 5)

        # send invalid data as POST form to endpoint (already added to pickup or delivery)
        response = app.test_client().get('/add-foodora')
        # check result from server with invalid data
        self.assertEqual(response.status_code, 400)


    

if __name__ == '__main__':
    unittest.main()