from flask import Flask,render_template,request

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index() :
	if request.method == "POST" :
		print(request.form)
	return render_template('editor_test.html')

@app.route("/save",methods=['GET','POST'])
def save() :
	if request.method == "POST" :
		#print(request.form['name'])
		print(typre(request.form))


@app.errorhandler(404)
def page(e) :
	return render_template('wrong.html')

@app.route('/test')
def t() :
	with open('templates/test.html','rb') as fi :
		rep = fi.read().decode('utf-8')
	return rep


if __name__ == '__main__' :

	app.run(debug=True,port=8000)