"""
Generates a synthetic e-commerce dataset used by both portfolio projects:
  01-sql-business-analysis
  02-bi-dashboard

Tables: customers, products, orders, order_items
Design mirrors a realistic online retail business with seasonality,
repeat customers, churn, and varying product margins -- enough
signal to support meaningful SQL analysis and dashboard KPIs.
"""
import random
import sqlite3
import csv
import os
from datetime import date, timedelta

random.seed(42)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIRS = [
    os.path.join(BASE_DIR, "01-sql-business-analysis", "data"),
    os.path.join(BASE_DIR, "02-bi-dashboard", "data"),
]

FIRST_NAMES = ["James","Mary","Robert","Patricia","John","Jennifer","Michael","Linda",
    "David","Elizabeth","William","Barbara","Richard","Susan","Joseph","Jessica",
    "Thomas","Sarah","Charles","Karen","Daniel","Nancy","Matthew","Lisa","Anthony",
    "Betty","Mark","Margaret","Donald","Sandra","Steven","Ashley","Paul","Kimberly",
    "Andrew","Emily","Joshua","Donna","Kenneth","Michelle"]
LAST_NAMES = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis",
    "Rodriguez","Martinez","Hernandez","Lopez","Gonzalez","Wilson","Anderson","Thomas",
    "Taylor","Moore","Jackson","Martin","Lee","Perez","Thompson","White","Harris",
    "Sanchez","Clark","Ramirez","Lewis","Robinson"]
CITIES = [("New York","NY"),("Los Angeles","CA"),("Chicago","IL"),("Houston","TX"),
    ("Phoenix","AZ"),("Philadelphia","PA"),("San Antonio","TX"),("San Diego","CA"),
    ("Dallas","TX"),("Austin","TX"),("Seattle","WA"),("Denver","CO"),("Boston","MA"),
    ("Atlanta","GA"),("Miami","FL"),("Portland","OR"),("Nashville","TN"),("Minneapolis","MN")]
CHANNELS = ["Organic Search","Paid Search","Email","Social Media","Direct","Referral"]
CATEGORIES = {
    "Electronics": [("Wireless Earbuds",39.99,14.00),("Bluetooth Speaker",59.99,22.00),
        ("Phone Case",19.99,4.50),("USB-C Charger",24.99,7.00),("Smart Watch",149.99,55.00),
        ("Laptop Stand",34.99,11.00)],
    "Home & Kitchen": [("Ceramic Mug Set",29.99,9.00),("Air Fryer",89.99,38.00),
        ("Cutting Board",22.99,6.50),("Throw Blanket",44.99,15.00),("Candle Set",26.99,8.00)],
    "Apparel": [("Cotton T-Shirt",18.99,5.00),("Denim Jacket",79.99,28.00),
        ("Running Shoes",99.99,35.00),("Wool Sweater",64.99,21.00),("Yoga Pants",44.99,13.00)],
    "Beauty": [("Face Serum",34.99,9.50),("Shampoo Bar",14.99,3.50),
        ("Makeup Brush Set",27.99,8.00),("Sunscreen SPF50",19.99,5.50)],
    "Sports & Outdoors": [("Yoga Mat",32.99,10.00),("Water Bottle",21.99,5.50),
        ("Camping Tent",129.99,48.00),("Resistance Bands",17.99,4.00)],
}

N_CUSTOMERS = 1200
START_DATE = date(2024, 1, 1)
END_DATE = date(2026, 6, 30)
TOTAL_DAYS = (END_DATE - START_DATE).days

def seasonal_weight(d):
    # Simple seasonality: bump in Nov-Dec (holidays) and July (summer sale)
    w = 1.0
    if d.month in (11, 12):
        w = 2.2
    elif d.month == 7:
        w = 1.5
    elif d.month in (1, 2):
        w = 0.75
    return w

def rand_date():
    for _ in range(20):
        offset = random.randint(0, TOTAL_DAYS)
        d = START_DATE + timedelta(days=offset)
        if random.random() < seasonal_weight(d) / 2.2:
            return d
    return START_DATE + timedelta(days=random.randint(0, TOTAL_DAYS))

# ---- Customers ----
customers = []
for cid in range(1, N_CUSTOMERS + 1):
    fn, ln = random.choice(FIRST_NAMES), random.choice(LAST_NAMES)
    city, state = random.choice(CITIES)
    signup = rand_date()
    segment = random.choices(["New","Returning","VIP"], weights=[0.45,0.4,0.15])[0]
    channel = random.choice(CHANNELS)
    customers.append({
        "customer_id": cid,
        "first_name": fn,
        "last_name": ln,
        "email": f"{fn.lower()}.{ln.lower()}{cid}@example.com",
        "city": city,
        "state": state,
        "signup_date": signup.isoformat(),
        "acquisition_channel": channel,
        "segment": segment,
    })

# ---- Products ----
products = []
pid = 1
for cat, items in CATEGORIES.items():
    for name, price, cost in items:
        products.append({
            "product_id": pid,
            "product_name": name,
            "category": cat,
            "unit_price": price,
            "unit_cost": cost,
        })
        pid += 1

# ---- Orders + Order Items ----
orders = []
order_items = []
order_id = 1
item_id = 1
STATUS_WEIGHTS = [("Completed",0.88),("Cancelled",0.07),("Returned",0.05)]

for c in customers:
    signup = date.fromisoformat(c["signup_date"])
    if c["segment"] == "VIP":
        n_orders = random.randint(6, 16)
    elif c["segment"] == "Returning":
        n_orders = random.randint(2, 6)
    else:
        n_orders = random.randint(1, 2)

    last_order_date = signup
    for _ in range(n_orders):
        gap = random.randint(5, 120)
        order_date = last_order_date + timedelta(days=gap)
        if order_date > END_DATE:
            break
        last_order_date = order_date

        status = random.choices([s for s,_ in STATUS_WEIGHTS], weights=[w for _,w in STATUS_WEIGHTS])[0]
        n_items = random.randint(1, 4)
        chosen_products = random.sample(products, n_items)
        order_total = 0.0
        items_for_order = []
        for p in chosen_products:
            qty = random.randint(1, 3)
            discount_pct = random.choices([0, 10, 15, 20], weights=[0.6,0.2,0.1,0.1])[0]
            line_price = round(p["unit_price"] * qty * (1 - discount_pct/100), 2)
            order_total += line_price
            items_for_order.append({
                "order_item_id": item_id,
                "order_id": order_id,
                "product_id": p["product_id"],
                "quantity": qty,
                "discount_pct": discount_pct,
                "line_total": line_price,
            })
            item_id += 1

        orders.append({
            "order_id": order_id,
            "customer_id": c["customer_id"],
            "order_date": order_date.isoformat(),
            "channel": c["acquisition_channel"],
            "status": status,
            "order_total": round(order_total, 2),
        })
        order_items.extend(items_for_order)
        order_id += 1

def write_csv(path, rows, fieldnames):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

for out_dir in OUT_DIRS:
    os.makedirs(out_dir, exist_ok=True)
    write_csv(os.path.join(out_dir, "customers.csv"), customers, list(customers[0].keys()))
    write_csv(os.path.join(out_dir, "products.csv"), products, list(products[0].keys()))
    write_csv(os.path.join(out_dir, "orders.csv"), orders, list(orders[0].keys()))
    write_csv(os.path.join(out_dir, "order_items.csv"), order_items, list(order_items[0].keys()))

# Build SQLite DB for project 1 (build in /tmp first -- mounted host folders
# can choke on sqlite's file-locking I/O, so we build locally then copy over)
import shutil
tmp_db_path = "/tmp/ecommerce_build.db"
db_path = os.path.join(OUT_DIRS[0], "ecommerce.db")
if os.path.exists(tmp_db_path):
    os.remove(tmp_db_path)
conn = sqlite3.connect(tmp_db_path)
cur = conn.cursor()
cur.execute("""CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, email TEXT,
    city TEXT, state TEXT, signup_date TEXT, acquisition_channel TEXT, segment TEXT)""")
cur.execute("""CREATE TABLE products (
    product_id INTEGER PRIMARY KEY, product_name TEXT, category TEXT,
    unit_price REAL, unit_cost REAL)""")
cur.execute("""CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT,
    channel TEXT, status TEXT, order_total REAL,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id))""")
cur.execute("""CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY, order_id INTEGER, product_id INTEGER,
    quantity INTEGER, discount_pct INTEGER, line_total REAL,
    FOREIGN KEY(order_id) REFERENCES orders(order_id),
    FOREIGN KEY(product_id) REFERENCES products(product_id))""")

cur.executemany("INSERT INTO customers VALUES (:customer_id,:first_name,:last_name,:email,:city,:state,:signup_date,:acquisition_channel,:segment)", customers)
cur.executemany("INSERT INTO products VALUES (:product_id,:product_name,:category,:unit_price,:unit_cost)", products)
cur.executemany("INSERT INTO orders VALUES (:order_id,:customer_id,:order_date,:channel,:status,:order_total)", orders)
cur.executemany("INSERT INTO order_items VALUES (:order_item_id,:order_id,:product_id,:quantity,:discount_pct,:line_total)", order_items)
conn.commit()
conn.close()
shutil.copyfile(tmp_db_path, db_path)

print(f"customers: {len(customers)}")
print(f"products: {len(products)}")
print(f"orders: {len(orders)}")
print(f"order_items: {len(order_items)}")
print("SQLite DB written to:", db_path)
