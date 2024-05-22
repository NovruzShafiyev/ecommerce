E-Commerce System with RESTful API 

Objective:
Develop an E-Commerce system that includes managing products, customers, and orders. Implement RESTful API endpoints to interact with the system.

Requirements:

Implement classes and create RESTful API endpoints using Flask
    - `GET /products`: Get a list of all products.
    - `POST /products`: Add a new product.
    - `GET /customers`: Get a list of all customers.
    - `POST /customers`: Add a new customer.
    - `POST /customers/<customer_id>/cart`: Add a product to the customer's cart.
    - `GET /customers/<customer_id>/cart`: View the customer's cart.
    - `POST /customers/<customer_id>/checkout`: Checkout the customer's cart and create an order.
    - `GET /orders`: Get a list of all orders.
