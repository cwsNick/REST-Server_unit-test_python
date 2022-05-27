# File: client.py

import client_crud

print("Product 1 Data:")
print(client_crud.get_product(0))

print("\nBuy product 1 , buy num 5:")
print(client_crud.buy_product(0, 5, "1234567890123456"))

print("Product 1 Data (After buy success):")
print(client_crud.get_product(0))

print("\nReplenish product 1 , Replenish product qty 5:")
print(client_crud.replenish_product(0, 5))