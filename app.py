from flask import Flask, request, redirect, session
from datetime import date
import sqlite3
app = Flask(__name__)
app.secret_key = "pharmacy_demo_key"

medicines = []
def init_db():
    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            expiry TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


init_db()

@app.route("/")
def login():
    return """
    <h1>Pharmacy Management System</h1>
    <h2>Login</h2>

    <form action="/login" method="post">
        <input name="username" placeholder="Username" required><br><br>
        <input name="password" type="password"
               placeholder="Password" required><br><br>
        <button type="submit">Login</button>
    </form>
    """


@app.route("/login", methods=["POST"])
def check_login():
    if (request.form["username"] == "admin"
            and request.form["password"] == "admin123"):
        session["user"] = "admin"
        return redirect("/dashboard")

    return "Invalid username or password. <a href='/'>Try Again</a>"


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return """
<html>
<head>
    <title>Pharmacy Dashboard</title>
</head>
<body style="font-family: Arial; text-align: center; background-color: #eaf7ea;">

    <h1 style="color: green;">Pharmacy Dashboard</h1>
    <h3>Welcome to Pharmacy Management System</h3>

    <br>

    <a href="/medicines">
        <button>Medicine Inventory</button>
    </a>

    <br><br>

    <a href="/expiry">
        <button>Expiry Date Tracking</button>
    </a>

    <br><br>

    <a href="/stock">
        <button>Low Stock Notifications</button>
    </a>

    <br><br>

    <a href="/prescription">
        <button>Prescription Validation</button>
    </a>

    <br><br>

    <a href="/billing">
        <button>Billing Management</button>
    </a>

    <br><br>

    <a href="/logout">
        <button>Logout</button>
    </a>

</body>
</html>
"""

@app.route("/medicines", methods=["GET", "POST"])
def inventory():
    if "user" not in session:
        return redirect("/")

    conn = sqlite3.connect("pharmacy.db")
    cursor = conn.cursor()
    if request.method == "POST":
        name = request.form["name"]
        quantity = 
    int(request.form["quantity"])
        expiry = request.form["expiry"]

        cursor.execute(
            "INSERT INTO medicines (name, quantity, expiry) VALUES (?, ?, ?)",
            (name, quantity, expiry)
        )

        conn.commit()
        conn.close()
        return redirect("/medicines")
    cursor.execute("SELECT name, quantity, expiry FROM medicines")
    saved_medicines = cursor.fetchall()
    conn.close()

    today = date.today().isoformat()
    rows = ""

    for medicine in saved_medicines:
        name, quantity, expiry = medicine

        if expiry < today:
            status = "EXPIRED - Do not dispense"
        elif expiry == today:
            status = "Expires today"
        elif quantity <= 10:
            status = "Low Stock"
        else:
            status = "Available"

        rows += f"""
        <tr>
            <td>{name}</td>
            <td>{quantity}</td>
            <td>{expiry}</td>
            <td>{status}</td>
        </tr>
        """

    return f"""
    <h1>Medicine Inventory</h1>

    <form method="post">
        <input name="name" placeholder="Medicine Name" required><br><br>

        <input name="quantity" type="number" min="0"
               placeholder="Tablet Quantity" required><br><br>

        <label>Expiry Date:</label>
        <input name="expiry" type="date" required><br><br>

        <button type="submit">Add Medicine</button>
    </form>

    <h2>Medicine Details</h2>

    <table border="1" cellpadding="8">
        <tr>
            <th>Medicine</th>
            <th>Quantity</th>
            <th>Expiry Date</th>
            <th>Status</th>
        </tr>
        {rows}
    </table>

    <br><a href="/dashboard">Back to Dashboard</a>
    """
@app.route("/expiry")
def expiry():
    if "user" not in session:
        return redirect("/")

    today = date.today().isoformat()
    expired = []

    for medicine in medicines:
        if medicine["expiry"] < today:
            expired.append(medicine)

    return f"""
    <h1>Expiry Date Tracking</h1>
    <p>Today's Date: {today}</p>
    <h2>Expired Medicines</h2>
    {''.join(
        f"<p>{m['name']} - Expiry: {m['expiry']}</p>"
        for m in expired
    ) or '<p>No expired medicines found.</p>'}
    <br>
    <a href="/dashboard">Back to Dashboard</a>
    """
@app.route("/stock")
def stock():
    if "user" not in session:
        return redirect("/")

    low_stock = [
        medicine for medicine in medicines
        if int(medicine["quantity"]) <= 10
    ]

    return f"""
    <h1>Low Stock Notification</h1>
    <h2>Medicines with Low Stock</h2>
    {''.join(
        f"<p>{m['name']} - Quantity: {m['quantity']}</p>"
        for m in low_stock
    ) or '<p>No low-stock medicines found.</p>'}
    <br>
    <a href="/dashboard">Back to Dashboard</a>
    """
@app.route("/prescription", methods=["GET", "POST"])
def prescription():
    if "user" not in session:
        return redirect("/")

    if request.method == "POST":
        prescription_id = request.form["prescription_id"]

        return f"""
        <h2>Prescription Submitted Successfully!</h2>
        <p>Prescription ID: {prescription_id}</p>
        <p>Please verify the prescription with a pharmacist.</p>
        <a href="/dashboard">Back to Dashboard</a>
        """

    return """
    <h1>Prescription Validation</h1>

    <form method="POST">
        <label>Prescription ID:</label>
        <input type="text" name="prescription_id" required>
        <button type="submit">Submit Prescription</button>
    </form>

    <br>
    <a href="/dashboard">Back to Dashboard</a>
    """
@app.route("/billing", methods=["GET", "POST"])
def billing():
    if "user" not in session:
        return redirect("/")

    result = ""

    if request.method == "POST":
        medicine_name = request.form["medicine"]
        quantity = int(request.form["quantity"])
        price = float(request.form["price"])

        total = quantity * price

        result = f"""
        <h3>Bill Generated Successfully!</h3>
        <p>Medicine: {medicine_name}</p>
        <p>Quantity: {quantity}</p>
        <p>Price per Tablet: ₹{price:.2f}</p>
        <h3>Total Amount: ₹{total:.2f}</h3>
        """

    return f"""
    <html>
    <head>
        <title>Pharmacy Billing</title>
    </head>
    <body style="font-family: Arial; text-align: center;
                 background-color: #e8f5e9; margin-top: 50px;">

        <h1>Pharmacy Billing</h1>

        <form method="POST">
            <label>Medicine Name:</label><br>
            <input type="text" name="medicine" required><br><br>

            <label>Quantity:</label><br>
            <input type="number" name="quantity" min="1" required><br><br>

            <label>Price per Tablet (₹):</label><br>
            <input type="number" name="price" min="0.01"
                   step="0.01" required><br><br>

            <button type="submit">Generate Bill</button>
        </form>

        {result}

        <br>
        <a href="/dashboard">Back to Dashboard</a>

    </body>
    </html>
    """
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
