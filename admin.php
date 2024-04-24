<?php

// Start or resume the session
session_start();

// Check if the user is logged in and has admin role
if (!(isset($_SESSION['logged_in']) && $_SESSION['logged_in'] && isset($_SESSION['role']) && $_SESSION['role'] === 'admin')) {
    // Redirect to index.php if not logged in as admin
    header("Location: index.php"); // Change index.php to your desired redirect page
    exit();
}

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Interface</title>
    <link rel="stylesheet" href="admin.css">
</head>
<body>

<!-- Category Form -->
<div class="form-container">
    <h2>Create New Category</h2>
    <form action="create_category.php" method="post">
        <input type="text" name="category_name" placeholder="Category Name" required>
        <button type="submit">Create Category</button>
    </form>
</div>

<!-- Subject Form -->
<div class="form-container">
    <h2>Upload New Subject</h2>
    <form action="upload_subject.php" method="post" enctype="multipart/form-data">
        <input type="text" name="subject_name" placeholder="Subject Name" required>
        <input type="file" name="subject_image" accept="image/*" required>
        <select name="categories[]" multiple required>
            <!-- Populate with existing categories -->
            <?php
            // Include the database configuration file
            require_once 'db_config.php';

            // Fetch existing categories from the database
            $sql = "SELECT * FROM categories";
            $result = $conn->query($sql);

            if ($result->num_rows > 0) {
                while ($row = $result->fetch_assoc()) {
                    echo "<option value='" . $row['category_id'] . "'>" . $row['category_name'] . "</option>";
                }
            }
            ?>
        </select>
        <button type="submit">Upload Subject</button>
    </form>
</div>

</body>
</html>
