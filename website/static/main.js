

var save_button = document.getElementById('save');
var error_text = document.getElementById('error-text');

function nameCheck(tag) {
    
    if(tag.value.length < 2){
        save_button.disabled = true;
        error_text.innerHTML = "Name should have atleast two characters";
        error_text.style.color = 'red';
        tag.style.borderColor = 'red';
    }
    else{
        save_button.disabled = false;
        error_text.innerHTML = " ";
        tag.style.borderColor = 'green';
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