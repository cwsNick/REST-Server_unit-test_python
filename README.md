# python-unit_test_min_assignment

## A list of file names and brief descriptions of the submitted files

| File Names          | Brief Descriptions                                          |
| ------------------- | ----------------------------------------------------------- |
| products.json       | Store products data                                         |
| server.py           | replenish a product to write or read products.json file.    |
| client.py           | Client program                                              |
| server_unit_test.py | Unit tests program                                          |
| client_crud.py      | Set JSON formats of the web service requests                |
| return_data.py      | Set JSON formats of the web service responses               |
| tools.py            | read, write JSON file and check_credit_card_number function |

## Instructions for setting up and executing the application

### Used third-party libraries: 
    
**Flask**

Use the following command to install Flask: 
```
pip3 install Flask
```

### Use the following command to execute the application:

1. start server program
```
python3 server.py
```
2. start client program
```
python3 client.py
```

### Instructions for setting up and executing the unit tests

Used third-party libraries: 
**Flask**

Use the following command to install Flask: 
```
pip3 install Flask
```

### Use the following command to execute the unit tests:

```
python3 server_unit_test.py
```

---

### JSON formats of the web service requests and responses

#### Additional and Delete API
| Name               | API URL        | HTTP Request Method | Call Server Function Name |
| ------------------ | -------------- | ------------------- | ------------------------- |
| Delete product API | /products/     | DELETE              | delete_product()          |
| Add product API    | /products/test | POST                | add_product()             |


### Query a product API
#### API URL
/products/

### HTTP Request Method 
GET
### JSON formatted requests:
| Key | Value      | Value Data type |
| --- | ---------- | --------------- |
| id  | product id | int             |

##### Example:
```
{ "id": 0 }
```

#### JSON formatted responses - success
| Key    | Value               | Value Data type |
| ------ | ------------------- | --------------- |
| desc   | product name        | String          |
| exe_id | Server execution ID | String          |
| id     | product name        | int             |
| price  | product price       | int             |
| qty    | product quantity    | int             |

##### Example:
```
{
"desc":"Apple",
"exe_id":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
"id":0,
   "price":10,
   "qty":200
}
```

#### JSON formatted responses - failure
| Key    | Value                | Value Data type |
| ------ | -------------------- | --------------- |
| exe_id | Server execution ID  | String          |
| status | Show status of query | String          |
| reason | Query failure reason | String          |

##### Example:
```
{	
"exe_id": exe_id(),
"status": "failure",
"reason": "id value invalid"
}
```

### Buy a product API
#### API URL
```
/products/
```

#### HTTP Request Method 
POST
#### JSON formatted requests
| Key             | Value              | Value Data type |
| --------------- | ------------------ | --------------- |
| id              | Sproduct id        | int             |
| buy_qty         | a quantity to buy  | int             |
| credit_card_num | credit-card number | String          |

##### Example:
```
{
   "id": 0,
   "buy_qty": 10,
   "credit_card_num":"1234567890123456"
}
```

#### JSON formatted responses - success
| Key      | Value                | Value Data type |
| -------- | -------------------- | --------------- |
| deducted | product name         | int             |
| exe_id   | Server execution ID  | String          |
| status   | Show status of query | String          |

##### Example:
```
{
"deducted":50,
   "exe_id":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
   "status":"success"
}
```

#### JSON formatted responses - failure
| Key    | Value                    | Value Data type |
| ------ | ------------------------ | --------------- |
| exe_id | Server execution ID      | String          |
| reason | Buy product fail reaseon | String          |
| status | Show status of buy       | String          |

##### Example:
```
{
 "exe_id":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
"reason":"quantity in stock smaller than the quantity to buy",
"status":"failure"
}
```

### Replenish a product API
#### API URL
```
/products/
```
#### HTTP Request Method 
PUT
#### JSON formatted requests
| Key           | Value              | Value Data type |
| ------------- | ------------------ | --------------- |
| id            | product  id        | int             |
| Replenish_qty | replenish quantity | int             |

##### Example:
```
{
   "id":0,
   "replenish_qty":10
}
```

#### JSON formatted responses - success
| Key                   | Value                                          | Value Data type |
| --------------------- | ---------------------------------------------- | --------------- |
| exe_id                | Server execution ID                            | String          |
| new quantity in stock | new product quantity in stock                  | int             |
| status                | status of Replenish product success or failure | String          |

##### Example:
```
{
   "exe_id":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
   "new quantity in stock":200,
   "status":"success"
}
```

#### JSON formatted responses - failure
| Key    | Value                                          | Value Data type |
| ------ | ---------------------------------------------- | --------------- |
| exe_id | Server execution ID                            | String          |
| status | status of replenish product success or failure | String          |
| status | reason of replenish product success or failure | String          |

##### Example:
```
{
   "exe_id":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
   "status":"failure",
   "reason":"replenish quantity should at least one"
}
```