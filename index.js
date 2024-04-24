function submitForm(url, form) {
    var formData = new FormData(form);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', url, true);
    xhr.onload = function () {
        if (xhr.status === 200) {
            // If login is successful, hide the popup
            if (xhr.responseText === 'success') {
                document.getElementById('popup').style.display = 'none';
            }
            alert(xhr.responseText); // Display response from server (replace with toast)
        } else {
            alert('Error: ' + xhr.statusText); // Display error message (replace with toast)
        }
    };
    xhr.onerror = function () {
        alert('Error: Network failure'); // Display error message (replace with toast)
    };
    xhr.send(formData);

    return false; // Prevent default form submission
}


document.addEventListener("DOMContentLoaded", function() {
    const loginBtn = document.getElementById("loginBtn");
    const popup = document.getElementById("popup");
    const loginForm = document.getElementById("loginForm");
    const registerForm = document.getElementById("registerForm");
    const registerInsteadBtn = document.getElementById("registerInsteadBtn");

    loginBtn.addEventListener("click", function() {
        popup.style.display = "flex"; // Display the popup when login button is clicked
    });

    registerInsteadBtn.addEventListener("click", function() {
        loginForm.style.display = "none";
        registerForm.style.display = "block";
    });
});




$(document).ready(function() {
    // Function to fetch and display subjects
    function fetchSubjects(category) {
        $.ajax({
            url: "subjectFetch.php",
            type: "GET",
            data: { category: category }, // Pass selected category to subjectFetch.php
            success: function(data) {
                $("#subjectContainer").html(data);
            },
            error: function(xhr, status, error) {
                console.error("Error fetching subjects:", error);
            }
        });
    }

    // Initial fetch of subjects when page loads
    fetchSubjects('');

    // Event listener for category selection
    $("#categoryPicker").change(function() {
        // Get the selected category
        var selectedCategory = $(this).val();
        // Fetch subjects for the selected category
        fetchSubjects(selectedCategory);
    });

    // Event listener for subject selection
    $(document).on("click", ".subjectImageContainer", function() {
        // Get the selected winner and loser
        var winner = $(this).find("img").attr("alt"); // Get the alt attribute of the clicked image
        var loser = $(this).siblings().find("img").attr("alt"); // Get the alt attribute of the other image
        var selectedCategory = $("#categoryPicker").val(); // Get the selected category
        
        // Submit the winner, loser, and selectedCategory data
        var formData = {
            winner: winner,
            loser: loser,
            category: selectedCategory
        };
        $.ajax({
            url: "EloRating.php",
            type: "POST",
            data: formData,
            success: function(data) {
                // Reload subjects after successful rating update
                fetchSubjects(selectedCategory); // Pass selected category to fetchSubjects
            },
            error: function(xhr, status, error) {
                console.error("Error updating ratings:", error);
            }
        });
    });
});
