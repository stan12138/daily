var editor = ace.edit("editor");
editor.setTheme("ace/theme/monokai");
editor.getSession().setMode("ace/mode/c_cpp");



var mode = document.getElementById("mode");
mode.onchange = function() {
	editor.getSession().setMode(mode.value);
}


var them = document.getElementById("theme");
them.onchange = function() {
	editor.setTheme(them.value);
}
