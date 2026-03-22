from flask import Flask, render_template, request, redirect

app = Flask(__name__)

users = []
cart = []

products = {
    "milk": [
        {"id": 1, "name": "Amul Milk", "price": 30, "image": "milk.png"},
        {"id": 2, "name": "Mother Dairy Milk", "price": 32, "image": "milk.png"},
        {"id": 3, "name": "Nestle Milk", "price": 35, "image": "milk.png"}
    ],
    "curd": [
        {"id": 4, "name": "Amul Curd", "price": 25, "image": "curd.png"},
        {"id": 5, "name": "Mother Dairy Curd", "price": 28, "image": "curd.png"}
    ],
    "butter": [
        {"id": 6, "name": "Amul Butter", "price": 55, "image": "butter.png"},
        {"id": 7, "name": "Britannia Butter", "price": 60, "image": "butter.png"}
    ],
    "cheese": [
        {"id": 8, "name": "Amul Cheese", "price": 80, "image": "cheese.png"},
        {"id": 9, "name": "Go Cheese", "price": 90, "image": "cheese.png"}
    ]
}

@app.route("/")
def home():
    return redirect("/register")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        users.append({
            "username": request.form["username"],
            "password": request.form["password"]
        })
        return redirect("/login")
    return render_template("register.html", cart=len(cart))

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        for u in users:
            if u["username"] == request.form["username"] and u["password"] == request.form["password"]:
                return redirect("/shop")
    return render_template("login.html", cart=len(cart))

@app.route("/shop")
def shop():
    return render_template("shop.html", cart=len(cart))

@app.route("/category/<name>")
def category(name):
    return render_template("category.html", items=products.get(name, []), category=name, cart=len(cart))

@app.route("/add/<int:id>")
def add(id):
    for c in products.values():
        for item in c:
            if item["id"] == id:
                for cart_item in cart:
                    if cart_item["id"] == id:
                        cart_item["qty"] += 1
                        return redirect("/cart")
                cart.append({"id": id, "name": item["name"], "price": item["price"], "qty": 1})
    return redirect("/cart")

@app.route("/inc/<int:id>")
def inc(id):
    for item in cart:
        if item["id"] == id:
            item["qty"] += 1
    return redirect("/cart")

@app.route("/dec/<int:id>")
def dec(id):
    for item in cart:
        if item["id"] == id:
            item["qty"] -= 1
            if item["qty"] <= 0:
                cart.remove(item)
    return redirect("/cart")

@app.route("/remove/<int:id>")
def remove(id):
    global cart
    cart = [item for item in cart if item["id"] != id]
    return redirect("/cart")

@app.route("/cart")
def view_cart():
    total = sum(item["price"] * item["qty"] for item in cart)
    return render_template("cart.html", cart_items=cart, total=total, cart=len(cart))

@app.route("/payment")
def payment():
    total = sum(item["price"] * item["qty"] for item in cart)
    return render_template("receipt.html", cart_items=cart, total=total, cart=len(cart))

if __name__ == "__main__":
    app.run()