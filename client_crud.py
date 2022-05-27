# File: client_crud.py
# R5. Unit tests - For test

import json
from urllib.request import Request, urlopen


SERVER = "127.0.0.1:5000"


# Client connect to server
def store_client(url, method=None, data=None):
    if not method:
        method = "POST" if data else "GET"
    if data:
        data = json.dumps(data).encode("utf-8")
    headers = {"Content-type": "application/json; charset=UTF-8"} \
        if data else {}
    req = Request(url=url, data=data, headers=headers, method=method)
    with urlopen(req) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    return result


# Query a product
def get_product(id):
    return store_client(f"http://{SERVER}/products/", "GET", {"id": id})

def get_product_requset():
    return store_client(f"http://{SERVER}/products/", "GET", {})


def get_all_product():
    return get_product("all")


# Buy Product
def buy_product(id, buy_qty, credit_card_num):
    json = {"id": id,
            "buy_qty": buy_qty,
            "credit_card_num": credit_card_num}
    return store_client(f"http://{SERVER}/products/", "POST", json)

def buy_product_null_requset():
    return store_client(f"http://{SERVER}/products/", "POST", {})

# Replenish a product
def replenish_product(id, replenish_qty):
    json = {"id": id,
            "replenish_qty": replenish_qty}
    return store_client(f"http://{SERVER}/products/", "PUT", json)


def replenish_product_null_requset():
    return store_client(f"http://{SERVER}/products/", "PUT", {})


# Delete product
def delete_product(id):
    return store_client(f"http://{SERVER}/products/", "DELETE", {"id": id})


# Add product
def add_product(id, desc, price, qty):
    return store_client(f"http://{SERVER}/products/test", "POST", {"id": id, "desc": desc, "price": price, "qty": qty})
