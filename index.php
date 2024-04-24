<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login/Register Popup</title>
    <link rel="stylesheet" href="index.css">
</head>
<body>

<!-- Universal Popup -->
<div id="popup" class="popup">
    <div id="loginForm">
        <h2>Login</h2>
        <form id="loginForm" action="login.php" method="post">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
            <button id="registerInsteadBtn">Register Instead?</button>
        </form>
    </div>
    <div id="registerForm" style="display: none;">
        <h2>Register</h2>
        <form id="registerForm" action="registration.php" method="post">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Register</button>
        </form>
    </div>
</div>

<!-- JavaScript for toggling between login and registration forms -->
<script src="index.js"></script>
</body>
</html>
