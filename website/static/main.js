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