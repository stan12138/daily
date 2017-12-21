var login_btn = document.getElementById("login-button");
if(login_btn){
    login_btn.onclick = ajax_handle_submit;
}
var httprequest;

function ajax_handle_submit(e) {
    var input_user = document.getElementById("user");
    var p1 = input_user.parentNode.previousElementSibling;
    var input_password = document.getElementById("password");
    var p2 = input_password.parentNode.previousElementSibling;
    if(input_user.value==""){
        p1.className += " has-error";
        input_user.className += " has-error";
    }
    else if(input_password.value==""){
        p1.className = "form-text";
        input_user.className = "side-form form-box";
        p2.className += " has-error";
        input_password.className += " has-error";
    }
    else{
        p1.className = "form-text";
        input_user.className = "side-form form-box";
        p2.className = "form-text";
        input_password.className = "side-form form-box";

        var form = document.getElementById("login-form");
        
        var form_data = new FormData(form);

        httprequest = new XMLHttpRequest();
        httprequest.onreadystatechange = ajax_handle_response;
        httprequest.open("POST", '/login');
        httprequest.send(form_data);
    }
}

function ajax_handle_response() {
    if(httprequest.readyState == 4 && httprequest.status == 200) {
        var change_part = document.getElementById("login-part");
        change_part.innerHTML = httprequest.responseText;
    }

    var logout_btn = document.getElementById("logout-button");
    if(logout_btn){
        logout_btn.onclick = ajax_logout;
    }

    var login_btn = document.getElementById("login-button");
    if(login_btn){
        login_btn.onclick = ajax_handle_submit;
    }
    var register_btn = document.getElementById("register-button");
    if(register_btn){
        register_btn.onclick = register;
    }

}


var logout_btn = document.getElementById("logout-button");
if(logout_btn){
    logout_btn.onclick = ajax_logout;
}
function ajax_logout(e) {
    var httpr = new XMLHttpRequest();
    httpr.onreadystatechange = ajax_logout_response;
    httpr.open('GET', '/logout');
    httpr.send();
}

function ajax_logout_response(e) {
    if(e.target.readyState == XMLHttpRequest.DONE && e.target.status == 200)
    {
        var change_part = document.getElementById("login-part");
        change_part.innerHTML = e.target.responseText;
    }

    var login_btn = document.getElementById("login-button");
    if(login_btn){
        login_btn.onclick = ajax_handle_submit;
    }

    var register_btn = document.getElementById("register-button");
    if(register_btn){
        register_btn.onclick = register;
    }
}

var register_btn = document.getElementById("register-button");
if(register_btn){
    register_btn.onclick = register;
}

function register() {
    var form = document.getElementById("login-form");
    var input_user = document.getElementById("user");
    var p1 = input_user.parentNode.previousElementSibling;
    var input_password = document.getElementById("password");
    var p2 = input_password.parentNode.previousElementSibling;
    if(input_user.value==""){
        p1.className += " has-error";
        input_user.className += " has-error";
    }
    else if(input_password.value==""){
        p1.className = "form-text";
        input_user.className = "side-form form-box";
        p2.className += " has-error";
        input_password.className += " has-error";
    }
    else{
        p1.className = "form-text";
        input_user.className = "side-form form-box";
        p2.className = "form-text";
        input_password.className = "side-form form-box";

        var form_data = new FormData(form);

        httprequest = new XMLHttpRequest();
        httprequest.onreadystatechange = ajax_handle_register_response;
        httprequest.open("POST", '/register');
        httprequest.send(form_data);
    }
}


function ajax_handle_register_response() {
    if(httprequest.readyState == 4 && httprequest.status == 200) {
        var change_part = document.getElementById("login-part");
        change_part.innerHTML = httprequest.responseText;
    }

    var logout_btn = document.getElementById("logout-button");
    if(logout_btn){
        logout_btn.onclick = ajax_logout;
    }

    var login_btn = document.getElementById("login-button");
    if(login_btn){
        login_btn.onclick = ajax_handle_submit;
    }
    var register_btn = document.getElementById("register-button");
    if(register_btn){
        register_btn.onclick = register;
    }

}