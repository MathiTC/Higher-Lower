document.addEventListener("DOMContentLoaded", function() {
    const loginForm = document.getElementById("loginForm");
    const registerForm = document.getElementById("registerForm");
    const registerInsteadBtn = document.getElementById("registerInsteadBtn");

    registerInsteadBtn.addEventListener("click", function() {
        loginForm.style.display = "none";
        registerForm.style.display = "block";
    });
});
