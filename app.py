from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

# 🌐 DATABASE CONFIGURATION
# You can set this via environment variable or hardcode it here for dev
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_LQATU7YkGmC4@ep-billowing-salad-a8miepz4-pooler.eastus2.azure.neon.tech/neondb?sslmode=require")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def create_table():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL
                )
            ''')
            conn.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    create_table()  # Ensures table exists on every request (optional)

    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute('INSERT INTO users (name) VALUES (%s)', (name,))
                    conn.commit()
        return redirect('/')

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM users')
            users = cur.fetchall()

    return render_template('index.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
