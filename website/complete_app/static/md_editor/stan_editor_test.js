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