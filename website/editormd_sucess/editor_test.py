from flask import Flask,render_template,request,Response

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def show() :
	if request.method == "POST" :
		print(request.form)
	return render_template('show.html')

@app.route('/test.md',methods=['GET','POST'])
def getmd() :
	with open("static/test1.md",'rb') as fi :
		rep = fi.read()
	return Response(rep,mimetype='text/markdown')

@app.route('/edit',methods=['GET','POST'])
def edit() :
	if request.method == "POST" :
		print(request.form)
	return render_template('editor.html')


@app.errorhandler(404)
def page(e) :
	return render_template('wrong.html')


if __name__ == '__main__' :

	app.run(host='0.0.0.0',debug=True,port=8000)