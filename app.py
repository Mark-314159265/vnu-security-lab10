import sqlite3
import os
from flask import Flask, request, session, redirect, url_for, render_template_string

app = Flask(__name__)
app.secret_key = "development-secret-key-vnu-lab"

def init_db():
    conn = sqlite3.connect("project.db")
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS users")
    cur.execute("DROP TABLE IF EXISTS orders")
    cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT, password TEXT, role TEXT)")
    cur.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER, item TEXT, amount REAL)")
    cur.executemany(
        "INSERT INTO users (email, password, role) VALUES (?, ?, ?)",
        [
            ("admin@vnu.edu.ua", "AdminSecure2026!", "admin"),
            ("student@vnu.edu.ua", "student2026", "user"),
        ]
    )
    cur.executemany(
        "INSERT INTO orders (user_id, item, amount) VALUES (?, ?, ?)",
        [
            (1, "Server Hardware License", 12500.0),
            (2, "Network Security Courseware", 450.0),
        ]
    )
    conn.commit()
    conn.close()

@app.route("/")
def index():
    q = request.args.get("q", "")
    conn = sqlite3.connect("project.db")
    cur = conn.cursor()
    if q:
        # ВРАЗЛИВІСТЬ SAST: пряма інтерполяція рядків у SQL-запит
        query = f"SELECT id, item, amount FROM orders WHERE item LIKE '%{q}%'"
        cur.execute(query)
    else:
        cur.execute("SELECT id, item, amount FROM orders")
    orders = cur.fetchall()
    conn.close()
    return f"<h1>Портал замовлень</h1><p>Знайдено: {len(orders)}</p>"

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email", "")
    password = request.form.get("password", "")
    conn = sqlite3.connect("project.db")
    cur = conn.cursor()
    # ВРАЗЛИВІСТЬ SAST: пряма конкатенація параметрів у SQL
    sql = f"SELECT id, email, role FROM users WHERE email = '{email}' AND password = '{password}'"
    cur.execute(sql)
    user = cur.fetchone()
    conn.close()
    if user:
        session["user"] = user[1]
        session["role"] = user[2]
        return "Вхід успішний"
    return "Невірні дані", 401

if __name__ == "__main__":
    init_db()
    # ВРАЗЛИВІСТЬ SAST: запущено режим відлагодження
    app.run(host="0.0.0.0", port=5000, debug=True)
