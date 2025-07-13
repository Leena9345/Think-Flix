# auth.py
from flask import current_app
import hashlib

mysql = None

def init_mysql(mysql_instance):
    global mysql
    mysql = mysql_instance

def hash_password(password):
    # Simple SHA256 hashing (consider stronger hashing in prod like bcrypt)
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    conn = mysql.connection
    cursor = conn.cursor()

    hashed_pw = hash_password(password)
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_pw))
        conn.commit()
        cursor.close()
        return True
    except Exception as e:
        print("Register error:", e)
        cursor.close()
        return False

def login_user(username, password):
    conn = mysql.connection
    cursor = conn.cursor()

    hashed_pw = hash_password(password)
    cursor.execute("SELECT id FROM users WHERE username=%s AND password=%s", (username, hashed_pw))
    user = cursor.fetchone()
    cursor.close()

    if user:
        return user[0]
    else:
        return None

def save_history(user_id, query, results_json):
    conn = mysql.connection
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO history (user_id, query, results) VALUES (%s, %s, %s)",
            (user_id, query, results_json)
        )
        conn.commit()
    except Exception as e:
        print("Error saving history:", e)
    finally:
        cursor.close()

def get_user_history(user_id):
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute(
        "SELECT query, results, timestamp FROM history WHERE user_id=%s ORDER BY timestamp DESC",
        (user_id,)
    )
    rows = cursor.fetchall()
    cursor.close()
    return rows
