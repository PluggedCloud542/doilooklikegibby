from flask import Flask, render_template, request, jsonify
import os

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
    testimonials_data = [
        {
            "text": "You look like Gibby from ICarly, exactly like him.",
            "author": "Ricky Berwick",
            "youtube_link": "https://www.youtube.com/embed/gMqAal7Qydc?si=k6JoX5_0550FgmRt"
        },
        {
            "text": "You got every little mark and roll on the body.",
            "author": "Hank Chill",
            "youtube_link": "https://www.youtube.com/embed/gxGvLW0nV2k?si=XeB8ZbMy4MerMwe-"
        },
        {
            "text": "How many hentai games do you have on your Nintendo Switch?",
            "author": "RGT85",
            "youtube_link": "https://www.youtube.com/embed/HgUZzRTT4pw?si=KYzCudalEPoMLMr_"
        },
        {
            "text": "",
            "author": "Eric Cartman",
            "youtube_link": ""
        },
        {
            "text": "You look like Gibby from iCarly. mmmmhmmmm.",
            "author": "John Crawley",
            "youtube_link": "https://www.youtube.com/embed/YHzdtdGJS5k?si=cDjQBZ5zAyfmzOhO"
        },
        {
            "text": "They could think maybe you suck, or maybe they think that you're awesomesauce and poggers. Who freaking knows? UWU. Poggers.",
            "author": "Jamishio",
            "youtube_link": "https://www.youtube.com/embed/OHkx9bJdb5E?si=jhrL7wjPka8-Iq1J"
        },
        {
            "text": "I hear you look a bit like Gibby from iCarly. Which I think is wonderful!",
            "author": "The Sexy Unicorn",
            "youtube_link": "https://www.youtube.com/embed/IPkISjxFAcc?si=s5T-rIUaSC3w95H1"
        },
        {
            "text": "Devin, by divine resemblance and public consensus, I hereby bestow upon you the ancient, revered, and mildly cursed title of Gibby, Lord of Chaos, shirtless herald of the north.",
            "author": "King Twink III",
            "youtube_link": "https://www.youtube.com/embed/kZDkl0Nr69I?si=k3RX7a-o3vxjs4cE"
        },
        {
            "text": "Not Carly but that other chick? She fine as hell.",
            "author": "Rooster",
            "youtube_link": "https://www.youtube.com/embed/Vub1wUjc1Mw"
        },
        {
            "text": "You look like Gibby. You look like Gibby. Do you want me to say it again?",
            "author": "Penny2Penthouse",
            "youtube_link": "https://www.youtube.com/embed/F4nB3toRm4w?si=7qBD_v9cW8Rmgag4"
        },
        {
            "text": "Hey Devin, you look like Gibby from iCarly.",
            "author": "Caleb Mulili",
            "youtube_link": "https://www.youtube.com/embed/olP_U8ATq_g?si=dd-2367-yihrWvqh"
        },
    ]
    return render_template('testimonials.html', testimonials=testimonials_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

