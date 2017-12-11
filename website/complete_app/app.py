from flask import Flask,render_template,request,Response

app = Flask(__name__)

@app.route('/',methods=['GET',])
def home() :
	return render_template('homepage.html')

@app.route("/code-editor",methods=['GET','POST'])
def code() :
	if request.method == "POST" :
		print(type(request.form))
	return render_template('code_editor.html')

@app.route("/save_code",methods=['POST',])
def save_code() :
	if request.method == "POST" :
		print(type(request.form))
	return render_template('code_editor.html')

@app.route('/md-editor/edit')
def md() :
	return render_template('md_editor_edit.html')

@app.route('/md-editor/show')
def md_show() :
	return render_template('md_editor_show.html')

@app.route('/md/test.md',methods=['GET','POST'])
def getmd() :
	with open("md/test1.md",'rb') as fi :
		rep = fi.read()
	return Response(rep,mimetype='text/markdown')


@app.errorhandler(404)
def page(e) :
	return render_template('wrong.html')

@app.route("/favicon.ico")
def icon() :
	with open("static/images/stan.ico",'rb') as fi :
		rep = fi.read()
	return Response(rep,mimetype='image/x-icon')


if __name__ == '__main__' :

	app.run(host="0.0.0.0",debug=True,port=8000)