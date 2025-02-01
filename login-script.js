// Placeholder for future login logic
document.querySelector('.login-form').addEventListener('submit', function(e) {
    e.preventDefault();
    // Add login logic here
});

// Predefined username and password
const validUsername = "Vicky";
const validPassword = "Vicky";

// Login form submission handler
document.getElementById("login-form").addEventListener("submit", function (event) {
    event.preventDefault();

    // Retrieve user inputs
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    // Authentication logic
    if (username === validUsername && password === validPassword) {
        // Successful login
        window.location.href = "http://localhost:8501/"; // Redirect to Main.html
    } else {
        // Display error message

        const errorMessage = document.getElementById("error-message");
        errorMessage.textContent = "Invalid username or password. Please try again.";
    }
});