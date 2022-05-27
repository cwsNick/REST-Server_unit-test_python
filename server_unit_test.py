# File: server_unit_test.py
# R5. Unit tests

from urllib.error import HTTPError
import unittest
import subprocess
import threading
import time
import client_crud

SERVER = "http://127.0.0.1:5000"


def create_temp_product(qty = 1000):
    products = client_crud.get_all_product()
    max_id = max(product['id'] for product in products) if products else 0

    temp_product = {"id": max_id + 1, "desc": "test", "price": 5, "qty": qty}
    client_crud.add_product(
        temp_product["id"], temp_product["desc"], temp_product["price"], temp_product["qty"])
    return temp_product


def test_get_product(self, id, http_status_code, msg):
    try:
        print(f"\n - {msg}")
        client_crud.get_product(id)
        self.assertTrue(False)  # should not reach this line
    except HTTPError as e:
        self.assertEqual(http_status_code, e.code)


def test_get_product_miss_invalid_data(self, id, msg):
    test_get_product(self, id, 400, msg)


def get_product_not_found(self, id, msg):
    test_get_product(self, id, 404, msg)


def test_buy_product(self, id, buy_qty, credit_card_num, http_status_code, msg):
    ole_products_len = len(client_crud.get_all_product())
    try:
        print(f"\n - {msg}")
        client_crud.buy_product(id, buy_qty, credit_card_num)
        self.assertTrue(False)  # should not reach this line
    except HTTPError as e:
        self.assertEqual(http_status_code, e.code)
    new_products_len = len(client_crud.get_all_product())
    self.assertEqual(ole_products_len, new_products_len)


def test_buy_product_miss_invalid_data(self, temp_product, buy_qty, card_num, msg):
    test_buy_product(self, temp_product["id"], buy_qty, card_num, 400, msg)

    # Buy product fails - qty in stock remains unchanged.
    new_stock_qty = client_crud.get_product(temp_product["id"])["qty"]
    self.assertEqual(temp_product["qty"], new_stock_qty)

    # Remove temporary product, if have
    client_crud.delete_product(temp_product["id"])


def buy_product_id_test(self, id, msg):
    ole_products_len = len(client_crud.get_all_product())
    test_buy_product(self, id, 1, "1234567890123456", 400, msg)
    new_products_len = len(client_crud.get_all_product())
    self.assertEqual(ole_products_len, new_products_len)


def buy_product_qty_test(self, buy_qty, msg):
    ole_products_len = len(client_crud.get_all_product())
    temp_product = create_temp_product()

    test_buy_product_miss_invalid_data(
        self, temp_product, buy_qty, "1234567890123456", msg)

    new_products_len = len(client_crud.get_all_product())
    self.assertEqual(ole_products_len, new_products_len)

    

def buy_product_card_num_test(self, card_num, msg):
    ole_products_len = len(client_crud.get_all_product())
    temp_product = create_temp_product()

    test_buy_product_miss_invalid_data(self, temp_product,
                                       temp_product["qty"], card_num, msg)

    new_products_len = len(client_crud.get_all_product())
    self.assertEqual(ole_products_len, new_products_len)


def test_buy_product_not_found(self, id, buy_qty, credit_card_num, msg):
    test_buy_product(self, id, buy_qty, credit_card_num, 404, msg)


def test_replenish_product(self, id, replenish_num, http_status_code, msg):
    try:
        print(f"\n - {msg}")
        client_crud.replenish_product(id, replenish_num)
        self.assertTrue(False)  # should not reach this line
    except HTTPError as e:
        self.assertEqual(http_status_code, e.code)


def test_replenish_product_miss_invalid_data(self, id, replenish_num, msg):
    ole_products_len = len(client_crud.get_all_product())
    test_replenish_product(self, id, replenish_num, 400, msg)
    new_products_len = len(client_crud.get_all_product())
    self.assertEqual(ole_products_len, new_products_len)


def test_replenish_product_qty_miss_invalid_data(self, replenish_num, msg):
    ole_products_len = len(client_crud.get_all_product())
    temp_product = create_temp_product()

    test_replenish_product(self, temp_product["id"], replenish_num, 400, msg)

    # Remove temporary product, if have
    client_crud.delete_product(temp_product["id"])

    new_products_len = len(client_crud.get_all_product())
    self.assertEqual(ole_products_len, new_products_len)


def test_404_replenish_product(self, id, replenish_num, msg):
    test_replenish_product(self, id, replenish_num, 404, msg)


class TestProductServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server_proc = subprocess.Popen(
            ["python3", "server.py"])
        time.sleep(0.5)

    @classmethod
    def tearDownClass(cls):
        cls.server_proc.terminate()


    def test_get_product_successful(self):
        # R5. query product returns the correct product attributes.
        print("Query Product")
        temp_product = create_temp_product()
        product = client_crud.get_product(temp_product["id"])

        self.assertTrue(product["id"] == temp_product["id"]
                        and product["desc"] == temp_product["desc"]
                        and product["price"] == temp_product["price"]
                        and product["qty"] == temp_product["qty"],
                        "Should same as temporary product")

        # Remove temporary product, if have
        client_crud.delete_product(temp_product["id"])

    # Not json request

    def test_get_product_failure(self):
        try:
            print("\n - Not JSON invalid")
            client_crud.get_product_requset()
            self.assertTrue(False)  # should not reach this line
        except HTTPError as e:
            self.assertEqual(400, e.code)

    # id invalid

    def test_get_product_failure(self):
        test_get_product_miss_invalid_data(
            self, None, "None id")        # 1) None id
        test_get_product_miss_invalid_data(
            self, "", "Empty String id")  # 2) Empty String id
        test_get_product_miss_invalid_data(
            self, "0", "String Num id")   # 3) String Num id
        test_get_product_miss_invalid_data(
            self, "abc", "String id")     # 4) String id
        test_get_product_miss_invalid_data(
            self, -1, "Negative id")      # 5) Negative id

        # 6) Product not found
        products = client_crud.get_all_product()
        max_id = max(product['id'] for product in products)
        get_product_not_found(self, max_id + 1, "Product not found")

    # R5. - Buying Product Successful

    def test_buy_product_successful(self):
        print("Test Buy Product - Successful")
        temp_product = create_temp_product()

        buy_qty = temp_product["qty"]
        credit_card_num = "1234567890123456"

        buy_result = client_crud.buy_product(
            temp_product["id"], buy_qty, credit_card_num)

        # Buy product success - qty in stock is updated.
        new_stock_qty = client_crud.get_product(temp_product["id"])["qty"]
        self.assertEqual(new_stock_qty, 0)

        # Check return data type
        self.assertEqual(type(buy_result["exe_id"]), str)
        self.assertEqual(type(buy_result["status"]), str)
        self.assertEqual(type(buy_result["deducted"]), int)

        self.assertTrue(buy_result["status"] == "success",
                        "Buy Product - Successful ")
        self.assertEqual(
            buy_result["deducted"], buy_qty * temp_product["price"])

        # Remove temporary product, if have
        client_crud.delete_product(temp_product["id"])

    # R5. - Buying Product Failure

    def test_buy_product_failure(self):
        print(" - Test Buy Product - Failure")
        print(" * buy_qty over stock qty}")
        ole_products_len = len(client_crud.get_all_product())
        temp_product = create_temp_product()
        
        result = client_crud.buy_product(temp_product["id"],temp_product["qty"] + 1 ,"1234567890123456")
        print(f"\n buy_product_qty_over_stock_test \n {result}")

        # Buy product fails - not enought qty in stock - qty in stock remains unchanged.
        new_stock_qty = client_crud.get_product(temp_product["id"])["qty"]
        self.assertEqual(temp_product["qty"], new_stock_qty)

        # Remove temporary product, if have
        client_crud.delete_product(temp_product["id"])

        new_products_len = len(client_crud.get_all_product())
        self.assertEqual(ole_products_len, new_products_len)
        

    # R5. - Input data are missing - no json request

    def test_buy_product_request_data_invalid(self):
        try:
            print("\n - Not JSON invalid")
            client_crud.buy_product_null_requset()
            self.assertTrue(False)  # should not reach this line
        except HTTPError as e:
            self.assertEqual(400, e.code)

    # R5. - Required input data are missing or invalid

    def test_buy_product_request_data_invalid(self):
        # id invalid
        # 1) None id
        buy_product_id_test(self, None, "None id")
        # 2) Null id string
        buy_product_id_test(self, "", "id is ''")
        # 3) String number
        buy_product_id_test(self, "0", "id is String num")
        # 4) String id
        buy_product_id_test(self, "abc", "id is String")
        # 5) Negative id
        buy_product_id_test(self, -1, "Negative id")

        # 6) id invalid - items not found
        card_num = "1234567890123456"

        products = client_crud.get_all_product()
        max_id = max(product['id'] for product in products)
        test_buy_product_not_found(self, max_id + 1, 1,
                                   card_num, "Product not found")

        # Buy Num
        # Negative buy_qty
        buy_product_qty_test(self, -30, "Buy num invalid - negative number")

        # buy_qty invalid - 0
        buy_product_qty_test(self,  0, "Buy num invalid - buy_qty == 0")

        # Credit Card Num
        buy_product_card_num_test(
            self, "abcd567890123456", "Credit card num invalid - Is not interget")
        # Is not interget

        buy_product_card_num_test(
            self, "123456789.0123456", "Credit card num invalid - Float Num")
        # Float num

        buy_product_card_num_test(
            self, "123", "Credit card num invalid - length is not 16")
        # Card num length is not 16

        buy_product_card_num_test(
            self, "-1234567890123456", "Credit card num invalid - Negative number")
        # Card num is negative number

    # Test Replenish Product SuccessFul

    def test_replenish_product_successful(self):
        print("Test Replenish Product SuccessFul")
        temp_product = create_temp_product()

        client_crud.replenish_product(temp_product["id"], 10)
        new_stock_qty = client_crud.get_product(temp_product["id"])["qty"]
        self.assertEqual(new_stock_qty, temp_product["qty"] + 10)

        # Remove temporary product, if have
        client_crud.delete_product(temp_product["id"])

    # Not json request

    def test_replenish_product_no_json_request(self):
        try:
            print("\n - Not JSON invalid")
            client_crud.replenish_product_null_requset()
            self.assertTrue(False)  # should not reach this line
        except HTTPError as e:
            self.assertEqual(400, e.code)

    def test_replenish_product_request_data_invalid(self):
        # id invalid
        test_replenish_product_miss_invalid_data(
            self, None, 1, "None id")          # 1) Null id
        # 2) Empty String id
        test_replenish_product_miss_invalid_data(self, "", 1, "id is ''")
        test_replenish_product_miss_invalid_data(
            self, "0", 1, "id is String num")  # 3) String number
        test_replenish_product_miss_invalid_data(
            self, "abc", 1, "id is String")    # 4) String id
        # 5) Negative id
        test_replenish_product_miss_invalid_data(self, -1, 1, "Negative id")

        # 6) Product not found
        products = client_crud.get_all_product()
        max_id = max(product['id'] for product in products)
        test_404_replenish_product(self, max_id + 1, 1, "Product Not Found")

        # replenish qty should at least one
        test_replenish_product_qty_miss_invalid_data(
            self, 0, "Replenish qty should at least one")
        
        
    
    def test_multi_requests_in_same_time(self):
        temp_product = create_temp_product(100)
        card_num = "1234567890123456"
        buy_qty = int(temp_product["qty"] / 2)
        print("\n\n ************test_multi_requests_in_same_time")
        
        threads = [threading.Thread(target=client_crud.buy_product, args=(temp_product["id"], buy_qty, card_num)) for i in range(2)]
        for t in threads: t.start()
        for t in threads: t.join()
        
        time.sleep(2)
        p = client_crud.get_product(temp_product["id"])
        new_product_qty = p["qty"]
        print(f"new_product_qty {new_product_qty}")
        self.assertEqual(0 , new_product_qty)
        
        # Remove temporary product, if have
        client_crud.delete_product(temp_product["id"])


if __name__ == "__main__":
    unittest.main()
