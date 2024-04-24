function fetchSubjectRankings(category) {
    $.ajax({
        url: "subjectRankings.php",
        type: "GET",
        data: { category: category },
        success: function(data) {
            $("#subjectRankings").html(data);
        },
        error: function(xhr, status, error) {
            console.error("Error fetching subject rankings:", error);
        }
    });
}

// Initial fetch of subject rankings when page loads
fetchSubjectRankings('');

// Event listener for category selection
$("#categoryPicker").change(function() {
    // Get the selected category
    var selectedCategory = $(this).val();
    // Fetch subjects for the selected category
    fetchSubjectRankings(selectedCategory);
});