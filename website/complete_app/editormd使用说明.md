# hello







编辑页面的请求



1.  jquery.min.js          html
2.  editormd.min.css            html
3.  stan_editor_test.js     html
4.  prettify.min.js          html
5.  raphael.min.js            html
6.  underscore.min.js         html
7.  sequence-diagram.min.js       html
8.  flowchart.min.js             html
9.  marked.min.js/                    html
10.  jquery.flowchart.min.js           html
11.  editormd.js                    html
12.  fontawesome-webfont.woff2        editormd.min.css
13.  editormd-logo.woff               editormd.min.css
14.  lib/codemirror/codemirror.min.css           codemirror的所有相关文件都由(editormd.js       102行path)决定，跟lib相关的都来自这里
15.  lib/codemirror/addon/dialog/dialog.css
16.  lib/codemirror/addon/search/matchesonscrollbar.css
17.  lib/codemirror/addon/fold/foldgutter.css
18.  lib/codemirror/codemirror.min.js
19.  lib/codemirror/modes.min.js
20.  lib/codemirror/addons.min.js
21.  lib/marked.min.js                              (editormd.js       102行path)
22.  lib/prettify.min.js
23.  lib/raphael.min.js
24.  lib/underscore.min.js
25.  lib/flowchart.min.js
26.  lib/jquery.flowchart.min.js
27.  lib/sequence-diagram.min.js
28.  katex.min.css           这个和下个都由editormd.js的4182与4181行决定
29.  katex.min.js





展示界面

test.md      html决定

这里的fontawesome，editormd相关的ttf，woff,woff2文件由editormd.preview.css的24行等决定

KaTeX_Main-Regular.woff2

Katex相关的字体由katex.min.css决定，你最好还是看一下请求的目录然后把字体文件夹放在她想要的目录，改一遍这个实在太麻烦了。