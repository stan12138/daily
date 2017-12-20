var editor = ace.edit("editor");
editor.setTheme("ace/theme/chrome");
editor.getSession().setMode("ace/mode/javascript");
var type_map = new Object();
var type_map = {
	javascript : ['.js', 'application/x-javascript'],
	c_cpp : ['.c', 'text/x-c'],
	css : ['.css', 'application/x-javascript'],
	html : ['.html', 'text/html'],
	java : ['.java', 'text/x-java-source'],
	latex : ['.tex', 'application/x-tex'],
	markdown : ['.md', 'text/x-markdown'],
	matlab : ['.m', 'text/x-m'],
	python : ['.py', 'text/x-script.python'],
	swift : ['.swift', 'text/plain'],
	text : ['.txt', 'text/pain']
};

var mode = document.getElementById("mode");
mode.onchange = function() {
	editor.getSession().setMode(mode.value);
	editor.setValue("");
	var res = mode.value.split("/")[2];
	var res1 = type_map[res];
	var suf = document.getElementById("suffix");
	suf.value = res1[0];
}


var them = document.getElementById("theme");
them.onchange = function() {
	editor.setTheme(them.value);
}

var save_button = document.getElementById("save-local");
save_button.onclick = function() {
	var name = document.getElementById("name");
	var pp = name.parentNode.previousElementSibling;
	if(name.value==""){
		name.className = "has-error";
		pp.className = "has-error";
	}
	else{
		name.className = "";
		pp.className = "";		
		var res = mode.value.split("/")[2];
		var res1 = type_map[res];
		var blob = new Blob([editor.getValue()],{type: res1[1]});
		saveAs(blob, name.value+res1[0]);
	}
}

var font_size = document.getElementById("font-size");
font_size.onchange = function() {
	document.getElementById("editor").style.fontSize=font_size.value;

}


var btn = document.getElementById("submit");
btn.onclick = function() {
	var fname = document.getElementById("name");
	var pp = fname.parentNode.previousElementSibling;
	var state = document.getElementById("state");

    var input_user = document.getElementById("user");
    var p1 = input_user.parentNode.previousElementSibling;
    var input_password = document.getElementById("password");
    var p2 = input_password.parentNode.previousElementSibling;

	if(fname.value.length<1){
		fname.className = "has-error";
		pp.className = "has-error";
	}
	else if(state.innerText=="Hello, stranger")
	{
		fname.className = "";
		pp.className = "";

        p1.className += " has-error";
        input_user.className += " has-error";
        p2.className += " has-error";
        input_password.className += " has-error";
    }
    else{

		fname.className = "";
		pp.className = "";
        p1.className = "form-text";
        input_user.className = "side-form form-box";
        p2.className = "form-text";
        input_password.className = "side-form form-box";

		var form = document.getElementById("form");
		var co = editor.getValue();
		var con = form.elements["content"];
		con.value = co;

		var res = mode.value.split("/")[2];
		var res1 = type_map[res];
		var fn = form.elements["filename"];
		fn.value = fname.value+res1[0]
		form.submit();
	}
}

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
}