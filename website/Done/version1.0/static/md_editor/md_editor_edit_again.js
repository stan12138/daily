$(function() {
        testEditor = editormd("test-editormd", {
            width        : "100%",//宽度
            height       : 720,//高度
            // 下面三个选项是设置风格的，每个有什么风格，请看下载插件得examples/themes.html
            theme        : "lesser-dark",// 工具栏风格
            //previewTheme : "dark",// 预览页面风格
            //editorTheme  : "paraiso-dark",// 设置编辑页面风格
            //path         : 'lib/',//这块是lib的文件路径，必须设置，否则几个样式css，js访问不到的
            flowChart : true,//控制流程图编辑
            sequenceDiagram : true,//控制时序图编辑
            taskList : true,//任务列表
            tex  : true,//科学公式
            emoji : true,//moji表情
            htmlDecode : "style,script,iframe|on*", // 开启 HTML 标签解析，为了安全性，默认不开启
            codeFold : true,//ctrl+q代码折叠
            saveHTMLToTextarea : true,//这个配置在simple.html中并没有，但是为了能够提交表单，使用这个配置可以让构造出来的HTML代码直接在第二个隐藏的textarea域中，方便post提交表单。这个转换好像有些缺陷，有些配置没有生效，目前还没想到怎么解决，我这里没有用,是在前台读取的时候转换的
            imageUpload : true,//开启本地图片上传
            imageFormats : ["jpg", "jpeg", "gif", "png", "bmp", "webp"],
            imageUploadURL : "/index.php/Admin/News/uploadFileMark",//图片上传地址
            onload : function() {
                console.log('onload', this);
            }
        });
        //设置可以添加目录，只需要在上面一行输入 [TOCM]，就会有目录，注意下面要空一行
        testEditor.config({
            tocm : true,
            tocContainer : "",
            tocDropdown   : false
        });
    });

var btn = document.getElementById("save");
btn.onclick = function() {
    var state = document.getElementById("state");
    try{
        var input_user = document.getElementById("user");
        var p1 = input_user.parentNode.previousElementSibling;
        var input_password = document.getElementById("password");
        var p2 = input_password.parentNode.previousElementSibling;
    }
    catch(error)
    {
        ;
    }
    
    if(state.innerText=="Hello, stranger")
    {
        try{
            p1.className += " has-error";
            input_user.className += " has-error";
            p2.className += " has-error";
            input_password.className += " has-error";
        } 
        catch(error)
        {
            ;
        }      
    }
    else
    {
        try{
            p1.className = "form-text";
            input_user.className = "side-form form-box";
            p2.className = "form-text";
            input_password.className = "side-form form-box";
        } 
        catch(error)
        {
            ;
        }  
        var form = document.getElementById("form");
        var con = document.getElementsByClassName('editormd-markdown-textarea');
        var con1 = con[0];
        var con2 = form.elements['content'];
        con2.value = con1.value;
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