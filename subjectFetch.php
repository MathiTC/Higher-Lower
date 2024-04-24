<?php
// Start or resume the session
session_start();

// Include the database configuration file
require_once 'db_config.php';

// Function to check if a user has already voted on a specific match
function hasVoted($conn, $userId, $winner, $loser) {
    $stmt = $conn->prepare("SELECT COUNT(*) AS count FROM user_votes WHERE user_id = ? AND subject1_id = ? AND subject2_id = ?");
    $stmt->bind_param("iii", $userId, $winner, $loser);
    $stmt->execute();
    $result = $stmt->get_result();
    $row = $result->fetch_assoc();
    $count = $row['count'];
    $stmt->close();
    return $count > 0;
}

// Check if the category is set
if (isset($_GET['category']) && !empty($_GET['category'])) {
    // Sanitize the category input
    $category = mysqli_real_escape_string($conn, $_GET['category']);
    
    // Fetch two random subjects from the specified category
    $sql = "SELECT subjects.subject_name, subjects.subject_image, subjects.subject_id 
            FROM subjects 
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
    // Fetch user ID from session (replace with actual session variable)
    $userId = $_SESSION['userid'] ?? 0;

    // Construct HTML for the subject container
    $html = '<div class="subjectContainer">';
    $subjectIds = array();
    while ($row = $result->fetch_assoc()) {
        $subject_name = $row['subject_name'];
        $subject_image = $row['subject_image'];
        $subject_id = $row['subject_id'];
        $subjectIds[] = $subject_id;
        // Add HTML for each image label
        $html .= '
            <label class="subjectImageContainer">            
                <img src="' . $subject_image . '" alt="' . $subject_id . '" class="subjectImage">
            </label>
        ';
    }
    $html .= '</div>';

    // Check if the subjects are different and the user hasn't voted on the match before
    if ($subjectIds[0] != $subjectIds[1] && !hasVoted($conn, $userId, $subjectIds[0], $subjectIds[1])) {
        echo $html;
    } else {
        echo '<p>No valid subjects found.</p>';
    }
} else {
    // Not enough subjects found
    echo '<p>No subjects found.</p>';
}

// Close statement and connection
$stmt->close();
$conn->close();
?>
