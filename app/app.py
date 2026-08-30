import os
import psycopg2
from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        database=os.environ.get("DB_NAME", "tododb"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", "postgres"),
        port=os.environ.get("DB_PORT", "5432")
    )
    return conn

def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id SERIAL PRIMARY KEY,
                task VARCHAR(255) NOT NULL
            );
        ''')
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Database connection error: {e}")

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>DevOps Task Manager</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f9; }
        .container { max-width: 500px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        h2 { text-align: center; color: #333; }
        ul { list-style-type: none; padding: 0; }
        li { padding: 10px; background: #eee; margin: 5px 0; border-radius: 4px; }
        input[type=text] { width: 70%; padding: 8px; }
        input[type=submit] { padding: 8px 15px; background: #28a745; color: white; border: none; border-radius: 4px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <h2>DevOps Todo List</h2>
        <form action="/add" method="POST">
            <input type="text" name="task" placeholder="New Task..." required>
            <input type="submit" value="Add">
        </form>
        <ul>
            {% for todo in todos %}
                <li>{{ todo[1] }}</li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    init_db()
    todos = []
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, task FROM todos;')
        todos = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error fetching tasks: {e}")
    return render_template_string(HTML_TEMPLATE, todos=todos)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    if task:
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('INSERT INTO todos (task) VALUES (%s);', (task,))
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(f"Error adding task: {e}")
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)