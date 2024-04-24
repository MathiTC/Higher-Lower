<?php
// Start or resume the session
session_start();

// Include the database configuration file
require_once 'db_config.php';

// Check if the form is submitted
if ($_SERVER["REQUEST_METHOD"] == "GET") {
    // Get the selected category from the request
    $category = $_GET["category"];

    // Determine the category to use in the SQL query
    $category_to_use = !empty($category) ? $category : "Global";

    // Construct the SQL query
    $sql = "SELECT subjects.subject_name, subjects.subject_image, elo_ratings.elo 
            FROM subjects
            LEFT JOIN elo_ratings ON subjects.subject_id = elo_ratings.subject_id 
            WHERE elo_ratings.category = ? 
            ORDER BY elo_ratings.elo DESC"; // Sort subjects by Elo rating in descending order

    // Prepare the SQL statement
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("s", $category_to_use); // Bind the category parameter

    // Execute the statement
    $stmt->execute();

    // Get the result
    $result = $stmt->get_result();

    // Display the subject rankings
    if ($result->num_rows > 0) {
        // Output subjects as images
        echo '<div class="subject-rankings">';
        $count = 0;
        while ($row = $result->fetch_assoc()) {
            // Output subject image and name
            echo '<div class="subject-item">';
            echo '<img src="' . $row['subject_image'] . '" alt="' . $row['subject_name'] . '" class="subject-image">';
            echo '<p>' . $row['subject_name'] . '</p>';
            echo '</div>';

            // Check if we've displayed 3 subjects
            $count++;
            if ($count % 3 == 0) {
                // Start a new row
                echo '</div>'; // Close previous row
                echo '<div class="subject-rankings">';
            }
        }
        echo '</div>'; // Close the last row
    } else {
        // No subjects found for the selected category
        echo '<p>No subjects found.</p>';
    }

    // Close the statement
    $stmt->close();
} else {
    // Request method is not GET
    echo "Invalid request method.";
}
?>
