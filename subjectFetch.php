<?php

// Include the database configuration file
require_once 'db_config.php';

// Check if the category is set
if (isset($_GET['category']) && !empty($_GET['category'])) {
    // Sanitize the category input
    $category = mysqli_real_escape_string($conn, $_GET['category']);
    
    // Fetch two random subjects from the specified category
    $sql = "SELECT subject_name, subject_image, subject_id FROM subjects 
            INNER JOIN subject_category ON subjects.subject_id = subject_category.subject_id 
            INNER JOIN categories ON subject_category.category_id = categories.category_id 
            WHERE categories.category_name = ? 
            ORDER BY RAND() 
            LIMIT 2";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("s", $category);
} else {
    // Fetch two random subjects without considering the category
    $sql = "SELECT subject_name, subject_image, subject_id FROM subjects 
            ORDER BY RAND() 
            LIMIT 2";
    $stmt = $conn->prepare($sql);
}

// Execute the query
$stmt->execute();
$result = $stmt->get_result();

// Check if at least two subjects are found
if ($result->num_rows >= 2) {
    // Construct HTML for the subject container
    $html = '<div class="subjectContainer">';
    while ($row = $result->fetch_assoc()) {
        $subject_name = $row['subject_name'];
        $subject_image = $row['subject_image'];
        $subject_id = $row['subject_id'];
        // Add HTML for each image label
        $html .= '
            <label class="subjectImageContainer">            
                <img src="' . $subject_image . '" alt="' . $subject_id . '" class="subjectImage">
            </label>
        ';
    }
    $html .= '</div>';
    echo $html;
} else {
    // Not enough subjects found
    echo '<p>No subjects found.</p>';
}

// Close statement and connection
$stmt->close();
$conn->close();
?>
