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

        // Prepare SQL statement to fetch the hashed password and role for the given username
        $stmt = $conn->prepare("SELECT password, role, id FROM users WHERE username = ?");
        $stmt->bind_param("s", $username);
        $stmt->execute();
        $result = $stmt->get_result();

        if ($result->num_rows > 0) {
            // Fetch the hashed password and role from the database
            $row = $result->fetch_assoc();
            $hashed_password = $row['password'];
            $role = $row['role'];
            $userId = $row['id'];

            // Verify the password against the hashed value
            if (password_verify($password, $hashed_password)) {
                // Login successful
                // Set session variables
                $_SESSION['username'] = $username;
                $_SESSION['logged_in'] = true;
                $_SESSION['role'] = $role;
                $_SESSION['userid'] = $userid;
                
                // Return success message to JavaScript
                echo "success";
            } else {
                // Login failed
                echo "Invalid username or password";
            }
        } else {
            // Username not found
            echo "Invalid username or password";
        }

        // Close statement
        $stmt->close();
    } else {
        echo "Please provide username and password";
    }
} else {
    // Redirect to index.php if the form is not submitted directly
    header("Location: index.php");
    exit();
}
?>
