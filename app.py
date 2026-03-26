from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "secret123"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lactocart.db"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

with app.app_context():
    db.create_all()

cart = []

# PRODUCTS (ALL DAIRY)
products = {
    "milk": [
        {"id":1,"name":"Amul Milk","price":30,"image":"milk.png"},
        {"id":2,"name":"Nestle Milk","price":35,"image":"milk.png"}
    ],
    "curd": [
        {"id":3,"name":"Amul Curd","price":25,"image":"curd.png"}
    ],
    "butter": [
        {"id":4,"name":"Amul Butter","price":55,"image":"butter.png"}
    ],
    "cheese": [
        {"id":5,"name":"Amul Cheese","price":80,"image":"cheese.png"}
    ],
    "paneer": [
        {"id":6,"name":"Fresh Paneer","price":90,"image":"cheese.png"}
    ],
    "ghee": [
        {"id":7,"name":"Desi Ghee","price":120,"image":"butter.png"}
    ]
}

@app.route("/")
def home():
    return redirect("/login")

# REGISTER
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method=="POST":
        user = User(username=request.form["username"],password=request.form["password"])
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    return render_template("register.html")

# LOGIN
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        user = User.query.filter_by(
            username=request.form["username"],
            password=request.form["password"]
        ).first()

        if user:
            session["user"]=user.username
            return redirect("/shop")

    return render_template("login.html")

# SHOP PAGE (CATEGORIES)
@app.route("/shop")
def shop():
    return render_template("shop.html", cart=len(cart))

# CATEGORY PAGE
@app.route("/category/<name>")
def category(name):
    items = products.get(name, [])
    return render_template("category.html", items=items, category=name, cart=len(cart))

# ADD TO CART
@app.route("/add/<int:id>")
def add(id):
    for cat in products.values():
        for item in cat:
            if item["id"]==id:
                cart.append(item)
                return redirect("/cart")
    return "Error"

# CART
@app.route("/cart")
def view_cart():
    total = sum(item["price"] for item in cart)
    return render_template("cart.html", cart_items=cart, total=total, cart=len(cart))

# PAYMENT
@app.route("/payment")
def payment():
    total = sum(item["price"] for item in cart)
    return render_template("receipt.html", cart_items=cart, total=total)

if __name__=="__main__":
    app.run(debug=True)