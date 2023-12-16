from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect('my_database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                score INTEGER NOT NULL
            )
        ''')
        conn.commit()

# Initialize the database
init_db()

@app.route('/')
def index():
    return "Welcome to my Flask app!"

@app.route('/submit-score', methods=['POST'])
def submit_score():
    score_data = request.json
    username = score_data['username']
    score = score_data['score']

    with sqlite3.connect('my_database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO scores (username, score) VALUES (?, ?)', (username, score))
        conn.commit()

    return jsonify({'status': 'success'})

@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    with sqlite3.connect('my_database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT username, score FROM scores ORDER BY score DESC LIMIT 10')
        top_scores = cursor.fetchall()

    return jsonify(top_scores)

if __name__ == '__main__':
    app.run(debug=True)
