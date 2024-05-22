document.addEventListener("DOMContentLoaded", function () {
  fetchProducts();
  fetchCustomers();
  fetchOrders();
});

function fetchProducts() {
  fetch("/products")
    .then((response) => response.json())
    .then((products) => {
      const productSelect = document.getElementById("product-select");
      const productList = document.getElementById("product-list");
      productSelect.innerHTML =
        '<option value="" disabled selected>Select Product</option>';
      productList.innerHTML = "";
      products.forEach((product) => {
        productSelect.innerHTML += `<option value="${product.id}">${product.name}</option>`;
        productList.innerHTML += `<li>${product.name} - $${product.price}</li>`;
      });
    });
}

function addProduct() {
  const name = document.getElementById("product-name").value;
  const price = document.getElementById("product-price").value;
  fetch("/products", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, price }),
  })
    .then((response) => response.json())
    .then((product) => {
      fetchProducts();
    });
}

function fetchCustomers() {
  fetch("/customers")
    .then((response) => response.json())
    .then((customers) => {
      const customerSelect = document.getElementById("customer-select");
      const customerList = document.getElementById("customer-list");
      customerSelect.innerHTML =
        '<option value="" disabled selected>Select Customer</option>';
      customerList.innerHTML = "";
      customers.forEach((customer) => {
        customerSelect.innerHTML += `<option value="${customer.id}">${customer.name}</option>`;
        customerList.innerHTML += `<li>${customer.name} - ${customer.email}</li>`;
      });
    });
}

function addCustomer() {
  const name = document.getElementById("customer-name").value;
  const email = document.getElementById("customer-email").value;
  fetch("/customers", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, email }),
  })
    .then((response) => response.json())
    .then((customer) => {
      fetchCustomers();
    });
}

function addToCart() {
  let customerId = document.getElementById("customer-select").value;
  let productId = document.getElementById("product-select").value;
  customerId = parseInt(customerId);
  productId = parseInt(productId);
  fetch(`/customers/${customerId}/cart`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ product_id: productId }),
  })
    .then((response) => response.json())
    .then((cart) => {
      viewCart();
    });
}

function viewCart() {
  let customerId = document.getElementById("customer-select").value;
  customerId = parseInt(customerId);
  fetch(`/customers/${customerId}/cart`)
    .then((response) => response.json())
    .then((cart) => {
      const cartList = document.getElementById("cart-list");
      cartList.innerHTML = "";
      cart.forEach((item) => {
        cartList.innerHTML += `<li>${item.name} - $${item.price}</li>`;
      });
    });
}

function checkout() {
  let customerId = document.getElementById("customer-select").value;
  customerId = parseInt(customerId);
  fetch(`/customers/${customerId}/checkout`, {
    method: "POST",
  })
    .then((response) => response.json())
    .then((order) => {
      fetchOrders();
      viewCart();
    });
}

function fetchOrders() {
  fetch("/orders")
    .then((response) => response.json())
    .then((orders) => {
      const orderList = document.getElementById("order-list");
      orderList.innerHTML = "";
      orders.forEach((order) => {
        orderList.innerHTML += `<li>Order #${order.id} by Customer ${order.customer_id} - Total: $${order.total}</li>`;
      });
    });
}
