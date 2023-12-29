var username = document.querySelector('#username');
var phone = document.querySelector('#phone');
var email = document.querySelector('#email');
var password = document.querySelector('#password');
var passconfirm = document.querySelector('#pass-confirm');
var form = document.querySelector('form');

function showError(input, message) {
    let parent = input.parentElement.parentElement;
    let small = parent.querySelector('small');
    parent.classList.add('error');
    small.innerText = message;
}
function showSuccess(input) {
    let parent = input.parentElement.parentElement;
    let small = parent.querySelector('small');
    parent.classList.remove('error');
    small.innerText = '';
}
function checkEmpty(input) {
    let isEmpty = false;
    input.value = input.value.trim();
    if(!input.value) {
        isEmpty = true;
        var errorMess
        if(input.id == 'username') {
            errorMess = `Vui lòng nhập tên đăng nhập.`;
        }
        if(input.id == 'phone') {
            errorMess = `Vui lòng nhập số điện thoại.`;
        }
        if(input.id == 'email') {
            errorMess = `Vui lòng email.`;
        }
        if(input.id == 'password') {
            errorMess = `Vui lòng nhập mật khẩu.`;
        }
        if(input.id == 'pass-confirm') {
            errorMess = `Vui lòng nhập lại mật khẩu.`;
        }
        showError(input, errorMess);
    }
    else {
        isEmpty = false;
        showSuccess(input);
    }
    return isEmpty;
}
function checkEmail(input) {
    const regexEmail = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    input.value = input.value.trim();
    let isEmailError = !regexEmail.test(input.value);
    if(regexEmail.test(input.value)) {
        showSuccess(input);
    }
    else {
        showError(input, 'Email không đúng định dạng.');
    }
    return isEmailError;
}
function checkLength(input, max) {
    input.value = input.value.trim();
    var errorMess;
    if(input.value.length < max) {
        if(input.id == 'username') {
            errorMess = `Tên đăng nhập phải lớn hơn ${max} ký tự`;
        }
        if(input.id == 'password') {
            errorMess = `Mật khẩu phải lớn hơn ${max} ký tự`;
        }
        showError(input, errorMess);
        return true
    }
    else {
        showSuccess(input)
    }
    return false
}
function checkPass(passwordInput, passconfirmInput) {
    if(passwordInput.value !== passconfirmInput.value) {
        showError(passconfirmInput, 'Mật khẩu không trùng khớp.');
        return true;
    }
    else {
        showSuccess(passconfirmInput);
    }
    return false;
}
function checkPhoneNumber(input) {
    const phonePattern = /^(?:\+\d{1,3}\s?)?(?:\d{1,4}[\s-]?){8,15}$/;
    input.value = input.value.trim();
    let isPhoneError = !phonePattern.test(input.value);
    if(phonePattern.test(input.value)) {
        showSuccess(input);
    }
    else {
        showError(input, 'Số máy quý khách vừa nhập là số máy không có thực.');
    }
    return isPhoneError;
}

$(document).ready(function () {
    $('#register-form').submit(function (event) {
        event.preventDefault();
        let isUsernameEmpty = checkEmpty(username);
        if(!isUsernameEmpty) {
            let isUsernameError = checkLength(username, 4);
        }
        let isPhonenumberEmpty = checkEmpty(phone);
        if(!isPhonenumberEmpty) {
            let isPhoneError = checkPhoneNumber(phone);
        }
        let isEmailEmpty = checkEmpty(email);
        if(!isEmailEmpty) {
            let isEmailError = checkEmail(email);
        }
        let isPassEmpty = checkEmpty(password);
        if(!isPassEmpty) {
            let isPasswordError = checkLength(password, 5);
        }
        let isPassCoEmpty = checkEmpty(passconfirm);
        if(!isPassCoEmpty) {
            let isPasswordMatch = checkPass(password, passconfirm);
        }
        if (isUsernameEmpty || isPhonenumberEmpty || isEmailEmpty || isPassEmpty || isPassCoEmpty)
            return;
        var csrfToken = $("[name=csrfmiddlewaretoken]").val();
        console.log($(this).serialize())
        $.ajax({
            type: 'POST',
            url: "/register/",  // Replace with the actual URL of your view
            data: $(this).serialize(),
            headers: {
                'X-CSRFToken': csrfToken  // Include CSRF token in the headers
            },
            success: function (data) {
                if (data.result){
                    window.location.replace("/login/");
                }
                else{
                    alert('there');
                    console.log('data:')
                    console.log(data);
                }
                
            },
            error: function (data) {
                alert('Form submission failed!');
            }
        });
    });
});