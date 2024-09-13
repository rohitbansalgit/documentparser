function update_pass(){
    old_pass = $('#old_password0').val();
    new_pass = $('#password0').val();
    confirm_pass = $('#cpassword0').val();
    if(old_pass == '' || new_pass == '' || confirm_pass == ''){
        var toastHTML = 'Please fill all the fields';
        M.toast({html: toastHTML, classes: 'rounded'});
        return;
    }
    if(new_pass != confirm_pass){
        var toastHTML = 'Passwords and confirm password do not match';
        M.toast({html: toastHTML, classes: 'rounded'});
        return;
    }
    //check password length
    if(new_pass.length < 6){
        var toastHTML = 'New password should be atleast 6 characters long';
        M.toast({html: toastHTML, classes: 'rounded'});
        return;
    }
    $.ajax({
        url: '/update_password',
        type: 'POST',
        data: {
            old_pass: old_pass,
            new_pass: new_pass
        },
        success: function(response){
            console.log(response);
            if(response.message == 'success'){
                var toastHTML = 'Password updated successfully';
                M.toast({html: toastHTML, classes: 'rounded'});
                $('#old_password0').val('');
                $('#password0').val('');
                $('#cpassword0').val('');
            } else {
                var toastHTML = 'Old password is incorrect';
                M.toast({html: toastHTML, classes: 'rounded'});
            }
        }
    });
}

function validate() {
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    //check format of email
    var email_regex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    if (!email.match(email_regex)) {
        var toastHTML = 'Invalid email format';
        M.toast({html: toastHTML, classes: 'rounded'});
        return false;
    }
    if (email == '' || password == '') {
        var toastHTML = 'Please fill all the fields';
        M.toast({html: toastHTML, classes: 'rounded'});
        return false;
    }
    $.ajax({
        url: '/',
        type: 'POST',
        data: {
            email: email,
            password: password
        },
        success: function(response){
            console.log(response);
            if(response.message == 'success'){
                window.location.href = '/dashboard';
            } else {
                var toastHTML = 'Email id or password is incorrect';
                M.toast({html: toastHTML, classes: 'rounded'});
            }
        }
    });
}

$(document).ready(function() {
    $('#input-file-now-custom-2').on('change', function() {
        var formData = new FormData($('#formValidate1')[0]); // Create a FormData object with the form data
        // Show the loader
        $('#count_prog').show();
        $('#count_result').hide();

        $.ajax({
            url: '/file_upload',
            type: 'POST',
            data: formData,
            processData: false, // Prevent jQuery from automatically processing the data
            contentType: false, // Prevent jQuery from setting the content type
            success: function(response) {
                console.log(response);
                if (response.message === 'success') {
                    console.log(response.data);

                    var char_count = response.data['char_count'];
                    var word_count = response.data['word_count'];
                    //click on textbox
                    $('#cword').val(word_count);
                    $('#cchar').val(char_count);
                    repeat_char = response.data['char_frequency'];
                    repeat_word = response.data['word_frequency'];
//                    console.log(repeat_char);
//                    let length = Object.keys(repeat_char).length;
                    // Assuming repeat_char is an object with key-value pairs
                    Object.keys(repeat_char).forEach(function(key, index) {
                        console.log(key);
                        // Create a new input element
                        let input = $('<input>', {
                            type: 'text',
                            class: 'validate',
                            id: 'repeat_char_' + index,
                            name: 'repeat_char_' + index,
                            value: '`'+key+'` frequency: '+repeat_char[key],
                            disabled: true
                        });

                        // Append the input element to the div with id 'repeat_char_container'
                        $('#repeat_char').append(input);
                    });

                    Object.keys(repeat_word).forEach(function(key, index) {
                        console.log(key);
                        // Create a new input element
                        let input = $('<input>', {
                            type: 'text',
                            class: 'validate',
                            id: 'repeat_char_' + index,
                            name: 'repeat_char_' + index,
                            value: '`'+key+'` frequency: '+repeat_word[key],
                            disabled: true
                        });

                        // Append the input element to the div with id 'repeat_char_container'
                        $('#repeat_word').append(input);
                    });

//                    var toastHTML = 'File uploaded successfully';
//                    M.toast({html: toastHTML, classes: 'rounded'});
                } else if (response.error === 'invalid_file_format') {
                    var toastHTML = 'Invalid file format. Only images, pdf, doc files are allowed';
                    M.toast({html: toastHTML, classes: 'rounded'});
                }
                $('#count_prog').hide();
                $('#count_result').show();
            },
            error: function() {
                var toastHTML = 'An error occurred while uploading the file';
                M.toast({html: toastHTML, classes: 'rounded'});
            }
        });
    });
});