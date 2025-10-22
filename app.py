from flask import Flask, render_template, request, jsonify, g
import os, json, sqlite3

app = Flask(__name__, template_folder='./ui', static_folder='./ui/static')

# --- SQLite setup ---
DATABASE = 'votes.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # allows dict-like access
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vote TEXT NOT NULL CHECK(vote IN ('yes', 'no'))
        )
    ''')
    db.commit()

with app.app_context():
    init_db()

# --- Voting functions ---
def save_vote_sqlite(vote):
    db = get_db()
    db.execute('INSERT INTO votes (vote) VALUES (?)', (vote,))
    db.commit()

def load_votes_sqlite():
    db = get_db()
    cursor = db.execute('SELECT vote, COUNT(*) as count FROM votes GROUP BY vote')
    counts = {'yes': 0, 'no': 0}
    for row in cursor:
        counts[row['vote']] = row['count']
    return counts['yes'], counts['no']

# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/saveVote', methods=['POST'])
def save_vote_route():
    data = request.get_json()
    vote = data.get('vote', '').strip().lower()
    if vote in ['yes', 'no']:
        save_vote_sqlite(vote)
        yes_votes, no_votes = load_votes_sqlite()
        return jsonify({'yes': yes_votes, 'no': no_votes})
    return jsonify({'error': 'Invalid vote'}), 400

@app.route('/getPollResults', methods=['GET'])
def get_poll_results():
    yes_votes, no_votes = load_votes_sqlite()
    return jsonify({'yes': yes_votes, 'no': no_votes})

@app.route('/testimonials')
def testimonials():
    with open('testimonials.json', 'r', encoding='utf-8') as f:
        testimonials_data = json.load(f)
    # Ignore disabled entries
    testimonials_data = [t for t in testimonials_data if not t.get('disabled')]
    return render_template('testimonials.html', testimonials=testimonials_data)
# --- Run app ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
