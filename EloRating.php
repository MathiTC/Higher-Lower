<?php
// Include the database configuration file
require_once 'db_config.php';

// Get the POST data
$winner = $_POST['winner'];
$loser = $_POST['loser'];
$category = $_POST['category']; // Category is optional, may be empty

// Check if category is set, otherwise set it to an empty string
if (empty($category)) {
    $category = 'Global';
}

// Default Elo rating
$defaultElo = 1000;

// Function to calculate Elo rating
function calculateElo($ratingWinner, $ratingLoser, $K, $result) {
    $expectationWinner = 1 / (1 + pow(10, ($ratingLoser - $ratingWinner) / 400));
    $expectationLoser = 1 / (1 + pow(10, ($ratingWinner - $ratingLoser) / 400));

    $newRatingWinner = $ratingWinner + $K * ($result - $expectationWinner);
    $newRatingLoser = $ratingLoser + $K * ((1 - $result) - $expectationLoser);

    return array('winner' => $newRatingWinner, 'loser' => $newRatingLoser);
}

// Function to update Elo rating in the database
function updateEloRating($conn, $subject_id, $category, $newElo) {
    $stmt = $conn->prepare("INSERT INTO elo_ratings (subject_id, category, ELO) VALUES (?, ?, ?) ON DUPLICATE KEY UPDATE ELO = ?");
    $stmt->bind_param("isii", $subject_id, $category, $newElo, $newElo);
    $stmt->execute();
    $stmt->close();
}

// Log user vote
function logUserVote($conn, $winner, $loser, $category) {
    $stmt = $conn->prepare("INSERT INTO user_votes (user_id, subject1_id, subject2_id, voted_subject_id, vote_timestamp) VALUES (?, ?, ?, ?, NOW())");
    // Replace 1 with the actual user ID once you have user authentication implemented
    $userId = $_SESSION['userid']; 
    $stmt->bind_param("iiii", $userId, $winner, $loser, $winner); // Assuming the winner's subject ID is logged
    $stmt->execute();
    $stmt->close();
}

// Get Elo ratings of winner and loser from the database
$stmtWinner = $conn->prepare("SELECT ELO FROM elo_ratings WHERE subject_id = ? AND category = ?");
$stmtWinner->bind_param("is", $winner, $category);
$stmtWinner->execute();
$resultWinner = $stmtWinner->get_result();
$rowWinner = $resultWinner->fetch_assoc();
$eloWinner = ($resultWinner->num_rows > 0) ? $rowWinner['ELO'] : $defaultElo;
$stmtWinner->close();

$stmtLoser = $conn->prepare("SELECT ELO FROM elo_ratings WHERE subject_id = ? AND category = ?");
$stmtLoser->bind_param("is", $loser, $category);
$stmtLoser->execute();
$resultLoser = $stmtLoser->get_result();
$rowLoser = $resultLoser->fetch_assoc();
$eloLoser = ($resultLoser->num_rows > 0) ? $rowLoser['ELO'] : $defaultElo;
$stmtLoser->close();

// Set Elo parameters
$K = 32; // Elo K-factor (adjustable)
$result = 1; // Winner is always 1, loser is 0

// Calculate new Elo ratings
$newElo = calculateElo($eloWinner, $eloLoser, $K, $result);

// Update Elo ratings in the database
updateEloRating($conn, $winner, $category, $newElo['winner']);
updateEloRating($conn, $loser, $category, $newElo['loser']);

// Log user vote
logUserVote($conn, $winner, $loser, $category);

// Close the database connection
$conn->close();

// Echo a success message
echo "Elo ratings updated successfully";
?>
