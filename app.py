from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "change-this-secret-key"
DB_PATH = Path(__file__).with_name("farmdirect.db")

PRODUCTS = [
    ("Fresh Tomatoes", 30.0, "kg", "🍅", "Vegetables"),
    ("Potatoes", 25.0, "kg", "🥔", "Vegetables"),
    ("Fresh Apples", 120.0, "kg", "🍎", "Fruits"),
    ("Bananas", 50.0, "dozen", "🍌", "Fruits"),
    ("Carrots", 40.0, "kg", "🥕", "Vegetables"),
    ("Green Broccoli", 60.0, "piece", "🥦", "Vegetables"),
    ("Fresh Spinach", 20.0, "bunch", "🥬", "Vegetables"),
    ("Mangoes", 90.0, "kg", "🥭", "Fruits"),
]

def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with connect_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                unit TEXT NOT NULL,
                icon TEXT NOT NULL,
                category TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL,
                items TEXT NOT NULL,
                total REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        count = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        if count == 0:
            conn.executemany(
                "INSERT INTO products (name, price, unit, icon, category) VALUES (?, ?, ?, ?, ?)",
                PRODUCTS
            )
        conn.commit()

@app.route("/")
def index():
    with connect_db() as conn:
        products = conn.execute("SELECT * FROM products ORDER BY category, name").fetchall()
    return render_template("index.html", products=products)

@app.route("/api/products")
def api_products():
    with connect_db() as conn:
        products = conn.execute("SELECT * FROM products ORDER BY id").fetchall()
    return jsonify([dict(p) for p in products])

@app.route("/checkout", methods=["POST"])
def checkout():
    customer_name = request.form.get("customer_name", "").strip()
    phone = request.form.get("phone", "").strip()
    address = request.form.get("address", "").strip()
    items_json = request.form.get("items", "")
    total_text = request.form.get("total", "0")

    if not customer_name or not phone or not address or not items_json:
        flash("Please fill in all customer details and add products to the cart.", "error")
        return redirect(url_for("index", _anchor="cart"))

    # Recalculate the total from server-side product prices rather than trusting the browser.
    import json
    try:
        requested_items = json.loads(items_json)
        if not isinstance(requested_items, list) or not requested_items:
            raise ValueError()
        order_lines = []
        total = 0.0
        with connect_db() as conn:
            for item in requested_items:
                product_id = int(item["id"])
                quantity = int(item["quantity"])
                if quantity < 1 or quantity > 100:
                    raise ValueError()
                product = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
                if product is None:
                    raise ValueError()
                line_total = product["price"] * quantity
                total += line_total
                order_lines.append(f'{product["name"]} x {quantity} = ₹{line_total:.2f}')
            conn.execute(
                "INSERT INTO orders (customer_name, phone, address, items, total) VALUES (?, ?, ?, ?, ?)",
                (customer_name, phone, address, "; ".join(order_lines), total)
            )
            conn.commit()
    except (ValueError, TypeError, KeyError, json.JSONDecodeError):
        flash("The cart details were invalid. Please review your cart and try again.", "error")
        return redirect(url_for("index", _anchor="cart"))

    flash(f"Demo order placed successfully! Your order number is #{conn.execute('SELECT last_insert_rowid()').fetchone()[0]}. No payment was collected.", "success")
    return redirect(url_for("index", _anchor="products"))

@app.route("/admin/orders")
def admin_orders():
    # For a classroom demo only. Add authentication before deploying publicly.
    with connect_db() as conn:
        orders = conn.execute("SELECT * FROM orders ORDER BY created_at DESC").fetchall()
    return render_template("orders.html", orders=orders)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
