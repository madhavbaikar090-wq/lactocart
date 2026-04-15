from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "secret123"

# ---------------- USERS ----------------
users = {}

# ---------------- PRODUCTS ----------------
products = {

    "milk": [
        {"name": "Amul Milk", "price": 30, "img": "milk.png"},
        {"name": "Mother Dairy Milk", "price": 32, "img": "milk.png"},
        {"name": "Nestle Milk", "price": 34, "img": "milk.png"}
    ],

    "curd": [
        {"name": "Amul Curd", "price": 40, "img": "curd.png"},
        {"name": "Nestle Curd", "price": 42, "img": "curd.png"}
    ],

    "butter": [
        {"name": "Amul Butter", "price": 55, "img": "butter.png"},
        {"name": "Britannia Butter", "price": 60, "img": "butter.png"}
    ],

    "cheese": [
        {"name": "Amul Cheese", "price": 65, "img": "cheese.png"},
        {"name": "Go Cheese", "price": 70, "img": "cheese.png"}
    ],

    "paneer": [
        {"name": "Amul Paneer", "price": 90, "img": "paneer.png"},
        {"name": "Mother Dairy Paneer", "price": 95, "img": "paneer.png"}
    ],

    "buttermilk": [
        {"name": "Amul Buttermilk", "price": 20, "img": "buttermilk.png"},
        {"name": "Chaas Masala", "price": 25, "img": "buttermilk.png"}
    ],

    "lassi": [
        {"name": "Sweet Lassi", "price": 30, "img": "lassi.png"},
        {"name": "Mango Lassi", "price": 40, "img": "lassi.png"}
    ],

    "icecream": [
        {"name": "Vanilla Ice Cream", "price": 60, "img": "icecream.png"},
        {"name": "Chocolate Ice Cream", "price": 70, "img": "icecream.png"}
    ],

    "ghee": [
        {"name": "Amul Ghee", "price": 120, "img": "ghee.png"},
        {"name": "Patanjali Ghee", "price": 115, "img": "ghee.png"}
    ],

    "flavoured_milk": [
    {"name": "Chocolate Milk", "price": 35, "img": "flavoured_milk.png"},
    {"name": "Strawberry Milk", "price": 38, "img": "flavoured_milk.png"}
],

"yogurt": [
    {"name": "Greek Yogurt", "price": 50, "img": "yogurt.png"},
    {"name": "Flavoured Yogurt", "price": 45, "img": "yogurt.png"}
],

"cream": [
    {"name": "Fresh Cream", "price": 60, "img": "cream.png"},
    {"name": "Whipping Cream", "price": 70, "img": "cream.png"}
],

"milk_powder": [
    {"name": "Amul Milk Powder", "price": 120, "img": "milk_powder.png"},
    {"name": "Nestle Milk Powder", "price": 130, "img": "milk_powder.png"}
],

"desserts": [
    {"name": "Rasgulla", "price": 80, "img": "desserts.png"},
    {"name": "Gulab Jamun", "price": 90, "img": "desserts.png"}
]
}

# ---------------- ROUTES ----------------

@app.route('/')
def home():
    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users[request.form['username']] = request.form['password']
        return redirect('/login')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']

        if u in users and users[u] == p:
            session['user'] = u
            session['cart'] = []
            return redirect('/shop')

    return render_template('login.html')


@app.route('/shop')
def shop():
    return render_template('shop.html')


@app.route('/products/<category>')
def show_products(category):
    if category not in products:
        return redirect('/shop')

    return render_template(
        'products.html',
        items=products[category],
        category=category
    )


@app.route('/add/<name>/<int:price>')
def add(name, price):
    if 'cart' not in session:
        session['cart'] = []

    session['cart'].append({
        "name": name,
        "price": price
    })

    session.modified = True
    return redirect('/cart')


@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    total = sum(item['price'] for item in cart)
    return render_template('cart.html', cart=cart, total=total)


@app.route('/payment')
def payment():
    cart = session.get('cart', [])
    total = sum(item['price'] for item in cart)
    return render_template('receipt.html', cart=cart, total=total)


if __name__ == '__main__':
    app.run(debug=True)