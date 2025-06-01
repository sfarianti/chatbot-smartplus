document.getElementById('sendBtn').addEventListener('click', function() {
    let userInput = document.getElementById('userInput').value;
    if (userInput) {
        displayMessage(userInput, 'user');  // Display user message on the right
        getChatbotResponse(userInput);
    }
});

function displayMessage(message, sender) {
    let messageDiv = document.createElement('div');
    messageDiv.classList.add(sender);  // Add the correct class ('user' or 'chatbot')
    messageDiv.textContent = message;
    document.getElementById('messages').appendChild(messageDiv);
    document.getElementById('userInput').value = '';  // Clear the input field
}

function getChatbotResponse(userInput) {
    fetch("/ask", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",  // Kirim data dalam format JSON
        },
        body: JSON.stringify({ user_input: userInput })  // Mengirim data sebagai JSON
    })
    .then(response => response.json())
    .then(data => {
        displayMessage(data.response, 'chatbot');  // Display chatbot response on the left
    });
}
