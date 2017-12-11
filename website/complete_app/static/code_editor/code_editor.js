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
	if(name.value==""){
		alert("请输入文件名");
	}
	else{
		var res = mode.value.split("/")[2];
		var res1 = type_map[res];
		var blob = new Blob([editor.getValue()],{type: res1[1]});
		saveAs(blob, name.value+res1[0]);
	}
}

var font_size = document.getElementById("font-size");
font_size.onchange = function() {
	var show_size = document.getElementById("show-size");
	var si = parseInt(font_size.value);
	show_size.value = font_size.value;
	var f_s = si + "%";
	document.getElementById("editor").style.fontSize=f_s;

}


var btn = document.getElementById("submit");
btn.onclick = function() {
	var fname = document.getElementById("name");
	if(fname.value==""){
		alert("请输入文件名");
	}
	else{
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