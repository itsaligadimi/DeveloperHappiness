from flask import Flask, render_template, request, redirect, g
import sqlite3

app = Flask(__name__)

DATABASE = 'developerhappiness.db'

# Initialize SQLite database
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tools (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                hashtags TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                tool TEXT NOT NULL,
                rating INTEGER NOT NULL,
                comment TEXT
            )
        ''')
        conn.commit()

init_db()

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    print("loading index")
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tools")
    tools = cursor.fetchall()
    cursor.execute("SELECT * FROM comments")
    comments = cursor.fetchall()
    return render_template('index.html', tools=tools, comments=comments)

@app.route('/add_comment', methods=['POST'])
def add_comment():
    name = request.form['name']
    tool = request.form['tool']
    rating = request.form['rating']
    comment = request.form['comment']
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO comments (name, tool, rating, comment) VALUES (?, ?, ?, ?)", (name, tool, rating, comment))
    db.commit()
    
    return redirect('/')

@app.route('/add_tool', methods=['POST'])
def add_tool():
    name = request.form['name']
    hashtags = request.form['hashtags']
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO tools (name, hashtags) VALUES (?, ?)", (name, hashtags))
    db.commit()
    
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
