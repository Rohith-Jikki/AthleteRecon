
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

