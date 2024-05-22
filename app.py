from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    total = db.Column(db.Float, nullable=False)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{'id': product.id, 'name': product.name, 'price': product.price} for product in products])

@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    new_product = Product(name=data['name'], price=data['price'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product added successfully!'}), 201

@app.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([{'id': customer.id, 'name': customer.name, 'email': customer.email} for customer in customers])

@app.route('/customers', methods=['POST'])
def add_customer():
    data = request.get_json()
    new_customer = Customer(name=data['name'], email=data['email'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer added successfully!'}), 201

@app.route('/customers/<int:customer_id>/cart', methods=['POST'])
def add_to_cart(customer_id):
    data = request.get_json()
    product_id = data['product_id']
    customer = Customer.query.get(customer_id)
    product = Product.query.get(product_id)
    if customer and product:
        new_cart_item = Cart(customer_id=customer_id, product_id=product_id)
        db.session.add(new_cart_item)
        db.session.commit()
        return jsonify({'message': 'Product added to cart successfully!'}), 201
    return jsonify({'message': 'Customer or Product not found'}), 404

@app.route('/customers/<int:customer_id>/cart', methods=['GET'])
def view_cart(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        cart_items = db.session.query(Cart, Product).join(Product).filter(Cart.customer_id == customer_id).all()
        cart_data = [{'name': product.name, 'price': product.price} for cart, product in cart_items]
        return jsonify(cart_data)
    return jsonify({'message': 'Customer not found'}), 404

@app.route('/customers/<int:customer_id>/checkout', methods=['POST'])
def checkout(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        cart_items = db.session.query(Cart, Product).join(Product).filter(Cart.customer_id == customer_id).all()
        if cart_items:
            total_price = sum(product.price for cart, product in cart_items)
            new_order = Order(customer_id=customer_id, total=total_price)
            db.session.add(new_order)
            # Clear the cart
            Cart.query.filter_by(customer_id=customer_id).delete()
            db.session.commit()
            return jsonify({'message': 'Checkout successful!'}), 201
        return jsonify({'message': 'Cart is empty'}), 400
    return jsonify({'message': 'Customer not found'}), 404

@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([{'id': order.id, 'customer_id': order.customer_id, 'total': order.total} for order in orders])

if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)
