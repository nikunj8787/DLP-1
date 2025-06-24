import pandas as pd
import sqlite3
import os

DB_FILE = "realestate.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            password TEXT,
            role TEXT,
            verified INTEGER DEFAULT 0
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            address TEXT,
            area TEXT,
            price TEXT,
            premise TEXT,
            bhk TEXT,
            furniture TEXT,
            property_age TEXT,
            contact_name TEXT,
            contact_phone TEXT,
            operator_email TEXT,
            status TEXT DEFAULT 'pending'
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS favorites (
            email TEXT,
            property_id INTEGER,
            PRIMARY KEY (email, property_id)
        )
    ''')
    conn.commit()
    conn.close()

def seed_users():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    users = [
        ("admin@demo.com", "admin123", "admin", 1),
        ("operator@demo.com", "operator123", "operator", 1),
        ("customer@demo.com", "customer123", "customer", 1),
    ]
    for u in users:
        c.execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?)", u)
    conn.commit()
    conn.close()

def check_user(email, password, role):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=? AND password=? AND role=? AND verified=1", (email, password, role))
    result = c.fetchone()
    conn.close()
    return result is not None

def add_user(email, password, role):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?, 0)", (email, password, role))
    conn.commit()
    conn.close()

def verify_user(email):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE users SET verified=1 WHERE email=?", (email,))
    conn.commit()
    conn.close()

def add_properties_from_csv(csv_file, operator_email):
    df = pd.read_csv(csv_file)
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    for _, row in df.iterrows():
        c.execute('''
            INSERT INTO properties
            (name, address, area, price, premise, bhk, furniture, property_age, contact_name, contact_phone, operator_email, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            row.get("Name & Contact", ""),
            row.get("Address", ""),
            row.get("Area", ""),
            row.get("Price", ""),
            row.get("Premise", ""),
            row.get("Premise", ""),
            row.get("Furniture & Other Details", ""),
            row.get("Property Age", ""),
            row.get("Name & Contact", ""),
            row.get("Phone Number", ""),
            operator_email,
            "pending"
        ))
    conn.commit()
    conn.close()

def get_properties(status=None, operator_email=None):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    query = "SELECT * FROM properties WHERE 1=1"
    params = []
    if status:
        query += " AND status=?"
        params.append(status)
    if operator_email:
        query += " AND operator_email=?"
        params.append(operator_email)
    c.execute(query, params)
    df = pd.DataFrame(c.fetchall(), columns=[x[0] for x in c.description])
    conn.close()
    return df

def update_property_status(property_id, status):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE properties SET status=? WHERE id=?", (status, property_id))
    conn.commit()
    conn.close()

def get_all_users(role=None, verified=None):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    query = "SELECT * FROM users WHERE 1=1"
    params = []
    if role:
        query += " AND role=?"
        params.append(role)
    if verified is not None:
        query += " AND verified=?"
        params.append(verified)
    c.execute(query, params)
    df = pd.DataFrame(c.fetchall(), columns=[x[0] for x in c.description])
    conn.close()
    return df

def add_favorite(email, property_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO favorites VALUES (?, ?)", (email, property_id))
    conn.commit()
    conn.close()

def get_favorites(email):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        SELECT properties.* FROM properties
        JOIN favorites ON properties.id = favorites.property_id
        WHERE favorites.email=?
    ''', (email,))
    df = pd.DataFrame(c.fetchall(), columns=[x[0] for x in c.description])
    conn.close()
    return df
