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
    // Check if subject name and image are set
    if (isset($_POST["subject_name"]) && isset($_FILES["subject_image"]["name"])) {
        // Sanitize subject name input (prevent SQL injection)
        $subject_name = htmlspecialchars($_POST["subject_name"]);

        // Check if image file is a actual image or fake image
        $check = getimagesize($_FILES["subject_image"]["tmp_name"]);
        if ($check !== false) {
            // Get image file extension
            $imageFileType = strtolower(pathinfo($_FILES["subject_image"]["name"], PATHINFO_EXTENSION));
            // Allow certain file formats
            if ($imageFileType != "jpg" && $imageFileType != "png" && $imageFileType != "jpeg" && $imageFileType != "gif") {
                echo "Sorry, only JPG, JPEG, PNG & GIF files are allowed";
            } else {
                // Check if categories are selected
                if (!empty($_POST["categories"])) {
                    $categories = $_POST["categories"];
                    // Upload image to server
                    $target_dir = "uploads/";
                    $target_file = $target_dir . basename($_FILES["subject_image"]["name"]);
                    if (move_uploaded_file($_FILES["subject_image"]["tmp_name"], $target_file)) {
                        // Prepare SQL statement to insert new subject into the database
                        $stmt = $conn->prepare("INSERT INTO subjects (subject_name, subject_image) VALUES (?, ?)");
                        $stmt->bind_param("ss", $subject_name, $target_file);
                        // Execute the statement
                        if ($stmt->execute()) {
                            // Get the last inserted subject id
                            $subject_id = $conn->insert_id;
                            // Insert subject-category mappings into the database
                            foreach ($categories as $category_id) {
                                $stmt = $conn->prepare("INSERT INTO subject_category (subject_id, category_id) VALUES (?, ?)");
                                $stmt->bind_param("ii", $subject_id, $category_id);
                                $stmt->execute();
                            }
                            echo "New subject uploaded successfully";
                        } else {
                            echo "Error: Subject upload failed";
                        }
                    } else {
                        echo "Error: Failed to upload image";
                    }
                } else {
                    echo "Please select at least one category";
                }
            }
        } else {
            echo "File is not an image";
        }
    } else {
        echo "Please provide subject name and image";
    }
} else {
    // Redirect to admin.php if the form is not submitted directly
    header("Location: admin.php");
    exit();
}
?>
