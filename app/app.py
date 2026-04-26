from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
 
app = Flask(__name__)
 
# Database path — stored in a Docker volume
DB_PATH = '/data/todos.db'
 
def init_db():
    """Initialize the database and create table if not exists"""
    os.makedirs('/data', exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            done BOOLEAN DEFAULT FALSE
        )
    ''')
    conn.commit()
    conn.close()
 
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
 
@app.route('/')
def index():
    conn = get_db()
    todos = conn.execute('SELECT * FROM todos').fetchall()
    conn.close()
    return render_template('index.html', todos=todos)
 
@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    if task:
        conn = get_db()
        conn.execute('INSERT INTO todos (task) VALUES (?)', (task,))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))
 
@app.route('/complete/<int:todo_id>')
def complete(todo_id):
    conn = get_db()
    conn.execute('UPDATE todos SET done = TRUE WHERE id = ?', (todo_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))
 
@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    conn = get_db()
    conn.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))
 
if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
