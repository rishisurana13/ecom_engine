# Ecommerce Engine (Specialized)
Welcome to this iteration of the ecommerce engines I am developing. This iteration is specialized in handling Jewelry-based
transactions. Unlike traditional e-commerce engines, the payment functionality is such that for every order there are two payements. In the jewelry industry, when an order is being commissioned, there is a initial downpayment. In the industry, this is referred to as an "advance" payment. This amount of this payment is usually determined by one or more of the following:
+ Gold Price
+ A percentage of the total item value
+ Labor based retainer

## How to Use 
1) Navigate to the root of the project.
2) Run ```source ecom_engine/bin/activate``` followed by ``` pip3 install -r requirements.txt```
3) Then run ```python3 manage.py runserver ``` to access the browsable API.
 **Please note you will need to use an extenstion like __modheader__ to attach the authentication token in the header for all user based actions.**



# Routes
| Verb(s) | URI Pattern            |
|---------|------------------------|
| POST    | `/sign-up`             |
| POST    | `/sign-in`             | 
| PATCH   | `/change-password`     | 
| DELETE  | `/sign-out`            | 
| POST, GET| `/products`            | 
| GET     | `/products/:id`        | 
| GET     | `/goals/:id`           | 
| PATCH   | `/goals/:id`           | 
| DELETE  | `/goals/:id`           | 


