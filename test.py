from flask import Flask, request, render_template
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# Database connection settings
DB_CONFIG = {
    'host': 'sql5.freesqldatabase.com',
    'user': 'sql5772904',
    'password': 'PW94CHIvYL',
    'database': 'sql5772904',
    'port': 3306
}

def get_connection():
    return mysql.connector.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database'],
        port=DB_CONFIG['port']
    )

@app.route("/")
def home():
    visitor_ip = request.remote_addr
    visit_time = datetime.now()

    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Insert IP and timestamp
        sql = "INSERT INTO visitor_log (ip_address, visit_time) VALUES (%s, %s)"
        cursor.execute(sql, (visitor_ip, visit_time))
        connection.commit()

    except mysql.connector.Error as err:
        print(f"Database error: {err}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
