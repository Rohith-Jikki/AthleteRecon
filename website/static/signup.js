$(document).ready(function() {

    // Listen for the change event on the select tag
    $('#club-or-player').change(function() {
      // Get the selected option value
      var selectedOption = $(this).val();
  
      // If Option 2 is selected, show the div; otherwise, hide it
      if (selectedOption == 'club') {
        $('.select-sport-container').hide();
        $('.gender').hide();
        $('#male-gender').removeAttr("required");
  
      } else {
        $('.select-sport-container').show();
        $('.gender').show();
      }
    });
  });

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

var check = function () {
            var password = document.getElementById('passwordInput');
            var cpassword = document.getElementById('confirmPasswordInput');
            var submit = document.getElementById('submit');
            var errors = document.getElementById('error-message');

            if(password.value.length < 7 ){
                errors.innerHTML = 'Enter 8 characters'
                errors.style.color = 'red'
            }
            else if(password.value.search(/[a-z]/i) < 0 || password.value.search(/[0-9]/) < 0){
                errors.innerHTML = 'weak'
                errors.style.color = 'red'
            }
            else if(password.value.search(/[!@#$%^&*]/) < 0){
                errors.innerHTML = 'moderate'
                errors.style.color = 'orange'
            }
            else{
                errors.innerHTML = 'strong'
                errors.style.color = 'green'
            }

            if (password.value == cpassword.value) {
                cpassword.style.borderColor = 'green';
                submit.disabled = false;
            } else {
                document.getElementById('confirmPasswordInput').style.borderColor = 'red';
                submit.disabled = true;

            }
        }

function readUrl(input){
  if(input.files && input.files[0]){
    var reader = new FileReader();
    reader.onload = function(e){
      $("#profile-picture-display").attr('src', e.target.result).width(100).height(100);

    };
    reader.readAsDataURL(input.files[0])
  }
}