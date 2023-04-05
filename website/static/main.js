$(document).ready(function() {
  // Hide the div on page load
  $('.cricket').hide();
  // Listen for the change event on the select tag
  $('#sport-select').change(function() {
    // Get the selected option value
    var selectedOption = $(this).val();

    // If Option 2 is selected, show the div; otherwise, hide it
    if (selectedOption == 'football') {
      $('.football').show();
      $('.cricket').hide();

    } else {
      $('.football').hide();
      $('.cricket').show();
    }
  });
});