from flask import Flask,render_template,request,Response,session,escape,redirect,url_for

app = Flask(__name__)

@app.route('/',methods=['GET',])
def home() :
	return render_template("home.html")

@app.route("/b1", methods=['POST',])
def b1() :
	print("get b1....")
	return 1

@app.route('/b2', methods=['POST',])
def b2() :
	print("this is b2")


if __name__ == "__main__" :
	app.run(host="0.0.0.0",port=8000)