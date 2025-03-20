from flask import Flask, request, jsonify
import psycopg2
import logging

app = Flask(__name__)

# Configuration (move to a separate file in a real app)
DB_ARGS = "dbname=testrequest user=postgres password=postgres host=localhost port=5433"
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Database functions
def conDB():
    conn = None
    try:
        conn = psycopg2.connect(DB_ARGS)
        logging.info("Connected to the database successfully.")
        return conn
    except psycopg2.Error as e:
        logging.error(f"Unable to connect to the database: {e}")
        return None

def insertUser(conn, name, age, mail, password):
    try:
        if conn is None:
            logging.error("No database connection available.")
            return False

        cur = conn.cursor()
        cur.execute('INSERT INTO "user" (name, age, mail, pass) VALUES (%s, %s, %s, %s)', (name, age, mail, password))
        conn.commit()
        logging.info("User added successfully.")
        return True
    except psycopg2.Error as e:
        logging.error(f"Error adding user: {e}")
        return False
    finally:
        if conn:
            cur.close()

def getUser(conn, name):
    try:
        if conn is None:
            logging.error("No database connection available.")
            return None

        cur = conn.cursor()
        cur.execute('SELECT * FROM "user" WHERE name = %s', (name,))
        user = cur.fetchone()

        if user:
            logging.info(f"User {name} retrieved successfully.")
            # Assuming columns are: name, age, mail, pass (adjust if different)
            user_data = {"name": user[0].strip(), "age": user[1].strip(), "mail": user[2].strip(), "password": user[3].strip()}
            return user_data
        else:
            logging.info(f"User {name} not found.")
            return None

    except psycopg2.Error as e:
        logging.error(f"Error retrieving user: {e}")
        return None
    finally:
        if conn:
            cur.close()


@app.route('/users/', methods=['POST'])
def create_user():
    data = request.get_json()

    if not data or not all(key in data for key in ("name", "age", "mail", "password")):
        return jsonify({"message": "Invalid request data"}), 400

    name = data["name"]
    age = data["age"]
    mail = data["mail"]
    password = data["password"]

    conn = conDB()
    if not conn:
        return jsonify({"message": "Database connection error"}), 500

    if insertUser(conn, name, age, mail, password):
        conn.close()
        return jsonify({"message": "User created successfully"}), 201
    else:
        conn.close()
        return jsonify({"message": "Failed to create user"}), 500

@app.route('/users/<name>', methods=['GET']) # Route for retrieving user by name
def get_user(name):
    conn = conDB()
    if not conn:
        return jsonify({"message": "Database connection error"}), 500

    user = getUser(conn, name)
    conn.close()

    if user:
        return jsonify(user), 200
    else:
        return jsonify({"message": "User not found"}), 404  # Not Found


if __name__ == '__main__':
    app.run(debug=True)