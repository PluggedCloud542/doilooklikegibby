const express = require('express');
const fs = require('fs');
const app = express();
const PORT = 3000;

let yesVotes = 0;
let noVotes = 0;

app.use(express.static(__dirname)); // Serve static files
app.use(express.json()); // Parse JSON bodies

// Load vote counts from file if it exists
const filePath = 'poll-results.txt';
if (fs.existsSync(filePath)) {
    const data = fs.readFileSync(filePath, 'utf8');
    data.split('\n').forEach(line => {
        if (line === 'Yes') yesVotes++;
        if (line === 'No') noVotes++;
    });
}

// Handle saving the vote
app.post('/saveVote', (req, res) => {
    const vote = req.body.vote;

    fs.appendFile('poll-results.txt', `${vote}\n`, (err) => {
        if (err) {
            console.error('Error saving vote:', err);
            return res.status(500).send('Error saving vote');
        }

        // Update vote counts
        if (vote === 'Yes') yesVotes++;
        if (vote === 'No') noVotes++;

        // Return the updated vote counts
        res.json({ yes: yesVotes, no: noVotes });
    });
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
