// Check if the user has already voted
window.onload = function() {
    if (localStorage.getItem('hasVoted')) {
        fetchResults();
    }
};

document.getElementById('pollForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const selectedOption = document.querySelector('input[name="poll"]:checked');
    
    if (selectedOption) {
        const vote = selectedOption.value;
        fetch('/saveVote', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ vote }),
        })
        .then(response => response.json())
        .then(data => {
            // Store that the user has voted
            localStorage.setItem('hasVoted', true);
            //ref
            setTimeout(() => {
                location.reload();
            }, 0); // Change delay (in milliseconds) as needed
            
            // Display thank you message and results
            document.getElementById('resultMessage').innerText = "Thank you for voting!";
            document.getElementById('pollForm').style.display = 'none';

            showResults(data);
        })
        .catch(error => {
            document.getElementById('resultMessage').innerText = "An error occurred.";
        });
    } else {
        document.getElementById('resultMessage').innerText = "Please select an option!";
    }
});

function showResults(data) {
    document.getElementById('pollResults').style.display = 'block';
    document.getElementById('yesVotes').innerText = `Yes: ${data.yes}`;
    document.getElementById('noVotes').innerText = `No: ${data.no}`;
}

// Fetch and display results if the user has already voted
function fetchResults() {
    fetch('/saveVote', { method: 'POST', body: JSON.stringify({ vote: "Check" }), headers: { 'Content-Type': 'application/json' } })
    .then(response => response.json())
    .then(data => {
        document.getElementById('resultMessage').innerText = "Thank you for voting!";
        document.getElementById('pollForm').style.display = 'none';

        showResults(data);

        document.getElementById('topImage').src = 'images/ohnogibby.jpg';
        document.getElementById('botImage').remove(); // New image 2
    })
    .catch(error => {
        document.getElementById('resultMessage').innerText = "An error occurred.";
    });
}
