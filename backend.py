from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import sql
import os

app = Flask(__name__)

# Database connection details from environment variables (set these in your env)
DB_HOST = os.getenv('DB_HOST', 'localhost')  # Replace with RDS endpoint
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'mydatabase')
DB_USER = os.getenv('DB_USER', 'admin')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'yourpassword')  # Secure this!

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

@app.route('/query', methods=['GET'])
def query_db():
    query_term = request.args.get('q', '')  # Get query parameter 'q'
    if not query_term:
        return jsonify({'error': 'No query provided'}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Safe parameterized query to prevent SQL injection
        sql_query = sql.SQL("SELECT * FROM items WHERE name ILIKE {}").format(sql.Literal('%' + query_term + '%'))
        cur.execute(sql_query)
        rows = cur.fetchall()

        # Convert rows to list of dicts
        results = [{'id': row[0], 'name': row[1]} for row in rows]

        cur.close()
        conn.close()

        return jsonify({'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)