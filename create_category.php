<?php
// Include the database configuration file
require_once 'db_config.php';

// Start or resume the session
session_start();

// Check if the user is logged in and has admin role
if (!(isset($_SESSION['logged_in']) && $_SESSION['logged_in'] && isset($_SESSION['role']) && $_SESSION['role'] === 'admin')) {
    // Redirect to index.php if not logged in as admin
    header("Location: index.php"); // Change index.php to your desired redirect page
    exit();
}

// Check if the form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Check if category name is set
    if (isset($_POST["category_name"])) {
        // Sanitize category name input (prevent SQL injection)
        $category_name = htmlspecialchars($_POST["category_name"]);

        // Prepare SQL statement to insert new category into the database
        $stmt = $conn->prepare("INSERT INTO categories (category_name) VALUES (?)");
        $stmt->bind_param("s", $category_name);

        // Execute the statement
        if ($stmt->execute()) {
            // Category creation successful
            echo "New category created successfully";
        } else {
            // Category creation failed
            echo "Error: Category creation failed";
        }

        // Close statement
        $stmt->close();
    } else {
        echo "Please provide category name";
    }
} else {
    // Redirect to admin.php if the form is not submitted directly
    header("Location: admin.php");
    exit();
}
?>
