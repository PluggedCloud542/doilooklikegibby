from flask import Flask, render_template, request, jsonify
import os, json

app = Flask(__name__, template_folder='./ui', static_folder='./ui/static')

# File to store poll results
RESULTS_FILE = 'poll-results.txt'

# Load votes from the file
def load_votes():
    yes_votes = 0
    no_votes = 0
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, 'r') as f:
            for line in f:
                if line.strip().lower() == 'yes':
                    yes_votes += 1
                elif line.strip().lower() == 'no':
                    no_votes += 1
    return yes_votes, no_votes

# Save a vote to the file
def save_vote(vote):
    with open(RESULTS_FILE, 'a') as f:
        f.write(vote + '\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/saveVote', methods=['POST'])
def save_vote_route():
    data = request.get_json()
    vote = data.get('vote', '').strip().lower()
    if vote in ['yes', 'no']:
        save_vote(vote)
        yes_votes, no_votes = load_votes()
        return jsonify({'yes': yes_votes, 'no': no_votes})
    return jsonify({'error': 'Invalid vote'}), 400

@app.route('/getPollResults', methods=['GET'])
def get_poll_results():
    yes_votes, no_votes = load_votes()
    return jsonify({'yes': yes_votes, 'no': no_votes})

@app.route('/testimonials')
def testimonials():
    with open('testimonials.json', 'r', encoding='utf-8') as f:
        testimonials_data = json.load(f)
    # Ignore disabled entries
    testimonials_data = [t for t in testimonials_data if not t.get('disabled')]
    return render_template('testimonials.html', testimonials=testimonials_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

