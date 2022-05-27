# File: return_data.py

from flask import Flask, jsonify
import hashlib
import socket
app = Flask(__name__)

student_name = "Chong Wan Si"
student_id = "12534001"


# R4. Server execution ID component - day time
def get_daytime(HOST, PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        data = s.recv(1024)
    return data.strip()


# R4. Server execution ID
def exe_id():
    return hashlib.sha256(get_daytime("time-a-g.nist.gov", 13)).hexdigest()

def null_JSON_request():
    return jsonify({"exe_id": exe_id(),
                    "status": "failure",
                    "reason": "Null JSON"}), 400

def id_invalid():
    return jsonify({"exe_id": exe_id(),
                    "status": "failure",
                    "reason": "id value invalid"}), 400


def get_one_product(product_id, desc, price, qty):
    return jsonify({"exe_id": exe_id(),
                    "id": product_id,
                    "desc": desc,
                    "price": price,
                    "qty": qty}), 200


def product_not_found():
    return jsonify({"exe_id": exe_id(),
                    "status": "failure",
                    "reason": "product item not found"}), 404


def buy_qty_should_at_least_one():
    return jsonify({"exe_id": exe_id(),
                    "status": "failure",
                    "reason": "buy qty should at least one"}), 400


def replenish_qty_at_least_one():
    return jsonify({"exe_id": exe_id(),
                    "status": "failure",
                    "reason": "replenish quantity should at least one"}), 400


def replenish_product_result(new_qty):
    return jsonify({"exe_id": exe_id(),
                    "status": "success",
                    "new quantity in stock": new_qty}), 200

def delete_product_result():
    return jsonify({"exe_id": exe_id(),
                    "status": "delete product success"}), 200
    
def add_product_failure():
    return jsonify({"exe_id": exe_id(),
                    "status": "failure",
                    "reason": "The id is used"}), 400
    
def add_product_result(JSON):
    return jsonify({"exe_id": exe_id(),
                    "status": "success",
                    "Added JSON": JSON}), 200

def buy_product_success(buy_qty, price):
    return jsonify({"exe_id": exe_id(),
                    "status": "success",
                    "deducted": buy_qty*price}), 200


def credit_card_num_invalid():
    return jsonify({"exe_id": exe_id(),
                    "status": "failure",
                    "reason": "credit card number invalid"}), 400


def inventory_shortage():
    return jsonify({"exe_id": exe_id(),
                    "status": "failure",
                    "reason": "quantity in stock smaller than the quantity to buy"}), 200
