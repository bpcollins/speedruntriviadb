from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client
import os

app = Flask(__name__)
CORS(app)


url = os.environ.get('SUPABASE_URL')
key = os.environ.get('SUPABASE_KEY')
supabase: Client = create_client(url, key)

@app.route('/')
def index():
    return "Welcome to my Flask app!"

@app.route('/submit-score', methods=['POST'])
def submit_score():
    score_data = request.json
    username = score_data['username']
    score = score_data['score']

    data = supabase.table("scores").insert({"username": username, "score": score}).execute()

    return jsonify({'status': 'success', 'data': data})

@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    data = supabase.table("scores").select("*").order("score", desc=True).limit(10).execute()

    return jsonify(data.get('data', []))

if __name__ == '__main__':
    app.run(debug=True)
