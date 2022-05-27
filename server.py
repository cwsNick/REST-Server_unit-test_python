# File: server.py
# R1 - R4

from flask import Flask, jsonify, request
import threading

# import python file
import return_data
import tools

app = Flask(__name__)
lock = threading.Lock()

json_file = "products.json"


# R2. Web service APIs - Query a product
@app.route("/products/", methods=["GET"])
def get_product():
    request_json = request.json
    if not request_json:
        return return_data.null_JSON_request()
    
    id = request_json["id"]

    products = tools.read_JSON_from_txt(json_file)

    if id == "all":
        return jsonify(products)

    # Input check
    if type(id) != int or id < 0:
        return return_data.id_invalid()

    for i, item in enumerate(products):
        if item["id"] == id:
            product = products[i]
            return return_data.get_one_product(
                product["id"], product["desc"],
                product["price"], product["qty"])
    return return_data.product_not_found()


# R2. Web service APIs - Buy a product
@app.route("/products/", methods=["POST"])
def buy_product():
    request_json = request.json
    if not request_json:
        return return_data.null_JSON_request()
    
    id = request_json["id"]
    buy_qty = request_json["buy_qty"]
    credit_card_num = request_json["credit_card_num"]

    # Input check
    if type(id) != int or id < 0:
        return return_data.id_invalid()

    if type(buy_qty) != int or buy_qty < 1:
        return return_data.buy_qty_should_at_least_one()

    if not tools.check_credit_card_number(credit_card_num):
        return return_data.credit_card_num_invalid()

    lock = threading.Lock()
    with lock:
        products = tools.read_JSON_from_txt(json_file)

        for item in products:  # loop for get item id
            if item["id"] == id:  # match item id

                # quantity in stock is insufficient
                if item["qty"] < int(buy_qty):
                    return return_data.inventory_shortage()

                # quantity in stock is sufficient
                else:
                    item["qty"] -= int(buy_qty)
                    tools.write_JSON_to_txt(json_file, products)

                    return return_data.buy_product_success(int(buy_qty), item["price"])
    return return_data.product_not_found()


# R2. Web service APIs - Replenish a product
lock.acquire()
@app.route("/products/", methods=["PUT"])
def replenish_product():
    request_json = request.json
    if not request_json:
        return return_data.null_JSON_request()
    
    id = request_json["id"]
    replenish_qty = request_json["replenish_qty"]

    # Input check
    if type(id) != int or id < 0:
        return return_data.id_invalid()
    if type(replenish_qty) != int or replenish_qty < 1:
        return return_data.replenish_qty_at_least_one()

    products = tools.read_JSON_from_txt(json_file)

    for item in products:  # loop for get item id
        if item["id"] == id:  # match item id
                        
            item["qty"] += replenish_qty
            tools.write_JSON_to_txt(json_file, products)
            
            return return_data.replenish_product_result(item["qty"])
    return return_data.product_not_found()

lock.release()


# For Unit tests
lock.acquire()
@app.route("/products/", methods=["DELETE"])
def delete_product():
    request_json = request.json
    if not request_json:
        return return_data.null_JSON_request()
    id = request_json["id"]

    # Input check
    if type(id) != int or id < 0:
        return return_data.id_invalid()

    products = tools.read_JSON_from_txt(json_file)

    for i, item in enumerate(products):
        if item["id"] == id:  # match item id
            products.pop(i)
            tools.write_JSON_to_txt(json_file, products)

            return return_data.delete_product_result()
    return return_data.product_not_found()
lock.release()


lock.acquire()
@app.route("/products/test", methods=["POST"])
def add_product():
    request_json = request.json
    if not request_json:
        return return_data.null_JSON_request()
    
    id = request_json["id"]
    desc = request_json["desc"]
    price = request_json["price"]
    qty = request_json["qty"]

    # Input check
    if type(id) != int or id < 0:
        return return_data.id_invalid()
    
    products = tools.read_JSON_from_txt(json_file)

    for item in products:
        if item["id"] == id:  # match item id
            return return_data.add_product_failure()

    json = {"id": id,
            "desc": desc,
            "price": price,
            "qty": qty}
    products.append(json)
    tools.write_JSON_to_txt(json_file, products)
    return return_data.add_product_result(json)
lock.release()


if __name__ == "__main__":
    app.run()
