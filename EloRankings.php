<?php
// Start or resume the session
session_start();

// Include database configuration
require_once 'db_config.php';

// Fetch categories from the database
$query = "SELECT * FROM categories";
$result = $conn->query($query);

// Store categories in an array
$categories = [];
if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $categories[] = $row['category_name'];
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Elo Rankings</title>
    <link rel="stylesheet" href="index.css">
</head>
<body>

<!-- Navbar -->
<nav class="navbar">
    <div class="navbar-logo">Your Logo</div>

    <!-- Category Picker -->
    <select id="categoryPicker" class="form-control">
        <option value="">Select Category</option>
        <?php foreach ($categories as $category) : ?>
            <option value="<?php echo $category; ?>"><?php echo $category; ?></option>
        <?php endforeach; ?>
    </select>
    <a href="index.php" class="button">Rating</a>
    <div>    
    <?php
    // Check if user is logged in
    if (!isset($_SESSION['logged_in'])) {
        // User is not logged in, display login button
        echo '<button id="loginBtn">Login</button>';
    } elseif ($_SESSION['role'] === 'admin') {
        // User is logged in as admin, display admin button
        echo '<p>' . $_SESSION['username'] . '</p>';
        echo '<a href="admin.php"><button>Admin</button></a>';
        echo '<a href="logout.php"><button>Logout</button></a>';
    } else {
        // User is logged in as a regular user, display username
        echo '<p>' . $_SESSION['username'] . '</p>';
        echo '<a href="logout.php"><button>Logout</button></a>';
    }
    ?>
    </div>
</nav>

<!-- Main Content -->
<main class="main-content">
    <div class="container">
        <!-- Subject Rankings -->
        <h3>Subject Rankings</h3>
        <div id="subjectRankings"></div>
    </div>
</main>

<!-- Universal Popup -->
<div id="popup" class="popup">
    <div class="popup-content" id="loginForm">
        <h2>Login</h2>
        <form id="loginForm" onsubmit="return submitForm('login.php', this);">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
            <button type="button" id="registerInsteadBtn">Register Instead?</button>
        </form>
    </div>
    <div class="popup-content" id="registerForm" style="display: none;">
        <h2>Register</h2>
        <form id="registerForm" onsubmit="return submitForm('registration.php', this);">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Register</button>
        </form>
    </div>
</div>

<!-- Javascript Files -->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script src="EloRankings.js"></script>
</body>
</html>