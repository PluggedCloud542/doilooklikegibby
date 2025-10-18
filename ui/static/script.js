// Check if the user has already voted
window.onload = function () {
    if (localStorage.getItem('hasVoted')) {
        // If the user has already voted, replace the images with an embedded YouTube video
        const imageContainer = document.querySelector('.image-container');
        imageContainer.innerHTML = `
            <div class="youtube-embed">
                <iframe width="560" height="315" src="https://www.youtube.com/embed/BGdsIWY9ckI?si=JKLcfd2koEmoI68-" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
            </div>
        `;

        // Hide the poll form and show the results
        document.getElementById('pollForm').style.display = 'none';
        document.getElementById('resultMessage').innerText = "You have already voted!";

        // Hide the "Show Results" button
        document.getElementById('showResultsButton').style.display = 'none';

        fetchResults();
    }
};

document.getElementById('pollForm').addEventListener('submit', function (event) {
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
                if (data.error) {
                    document.getElementById('resultMessage').innerText = "An error occurred.";
                    return;
                }
                // Store that the user has voted
                localStorage.setItem('hasVoted', true);

                // Replace the images with an embedded YouTube video
                const imageContainer = document.querySelector('.image-container');
                imageContainer.innerHTML = `
                    <div class="youtube-embed">
                        <iframe width="560" height="315" src="https://www.youtube.com/embed/64SaGa1Xu5c?si=m4fgzlUHzet9_jmd" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
                    </div>
                `;

                // Display thank you message and results
                document.getElementById('resultMessage').innerText = "Thank you for voting!";
                document.getElementById('pollForm').style.display = 'none';

                // Hide the "Show Results" button
                document.getElementById('showResultsButton').style.display = 'none';

                showResults(data);
            })
            .catch(error => {
                document.getElementById('resultMessage').innerText = "An error occurred.";
            });
    } else {
        document.getElementById('resultMessage').innerText = "Please select an option!";
    }
});

// Show the results when the "Show Results" button is clicked
document.getElementById('showResultsButton').addEventListener('click', function () {
    fetchResults();
});

function fetchResults() {
    fetch('/getPollResults', {
        method: 'GET',
    })
        .then(response => response.json())
        .then(data => {
            showResults(data);
        })
        .catch(error => {
            document.getElementById('resultMessage').innerText = "An error occurred while fetching results.";
        });
}

function showResults(data) {
    document.getElementById('pollResults').style.display = 'block';
    document.getElementById('yesVotes').innerText = `Yes: ${data.yes}`;
    document.getElementById('noVotes').innerText = `No: ${data.no}`;
}