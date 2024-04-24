<?php
// Include the database configuration file
require_once 'db_config.php';

// Start or resume the session
session_start();

// Check if the form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Check if username and password are set
    if (isset($_POST["username"]) && isset($_POST["password"])) {
        // Sanitize user inputs (prevent SQL injection)
        $username = htmlspecialchars($_POST["username"]);
        $password = htmlspecialchars($_POST["password"]);

        // Check if the username is already taken
        $stmt_check = $conn->prepare("SELECT * FROM users WHERE username = ?");
        $stmt_check->bind_param("s", $username);
        $stmt_check->execute();
        $result = $stmt_check->get_result();

        if ($result->num_rows > 0) {
            // Username already taken
            echo "Error: Username already taken";
        } else {
            // Hash the password using the best industry standard
            $hashed_password = password_hash($password, PASSWORD_DEFAULT);

            // Prepare SQL statement to insert new user into the database
            $stmt_insert = $conn->prepare("INSERT INTO users (username, password) VALUES (?, ?)");
            $stmt_insert->bind_param("ss", $username, $hashed_password);

            // Execute the statement
            if ($stmt_insert->execute()) {
                // Registration successful
                // Set session variables
                $_SESSION['username'] = $username;
                $_SESSION['logged_in'] = true;
                $_SESSION['role'] = 'user';

                // Echo success message to indicate successful registration
                echo "success";
            } else {
                // Registration failed
                echo "Error: Registration failed";
            }

            // Close statement
            $stmt_insert->close();
        }

        // Close check statement
        $stmt_check->close();
    } else {
        echo "Please provide username and password";
    }
} else {
    // Redirect to index.php if the form is not submitted directly
    header("Location: index.php");
    exit();
}
?>
