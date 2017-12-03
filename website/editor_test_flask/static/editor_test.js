var editor = ace.edit("editor");
editor.setTheme("ace/theme/monokai");
editor.getSession().setMode("ace/mode/python");

var btn = document.getElementById("submit");

btn.onclick = function() {
	var form = document.getElementById("form1");
	var co = editor.getValue();
	alert(co);
	var con = form.elements["content"];
	con.value = co;

	form.submit();
}

var mode = document.getElementById("mode");
mode.onchange = function() {
	alert(mode.value);
	editor.getSession().setMode(mode.value);
}


var them = document.getElementById("theme");
them.onchange = function() {
	alert(them.value);
	editor.setTheme(them.value);
}