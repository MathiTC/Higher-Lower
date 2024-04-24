<?php
// Database configuration constants
define('DB_HOST', 'localhost');
define('DB_NAME', 'arosappa_HLR');
define('DB_USER', 'arosappa_HighLowRating');
define('DB_PASS', 'p8V:@?tEAWegrD=]zyn8');

// Create a MySQLi instance for database connection
$conn = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
?>
