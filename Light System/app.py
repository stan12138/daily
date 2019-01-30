from flask import Flask,render_template,request,Response,session,escape,redirect,url_for
import serial
import time

app = Flask(__name__)

s=serial.Serial("/dev/ttyACM0", 9600, timeout=5)

def send_message(x) :
	pass
	s.write(str(x).encode("utf-8"))

@app.route('/',methods=['GET',])
def home() :
	return render_template("home.html")

@app.route("/b1", methods=['POST',])
def b1() :
	send_message(1)
	return render_template("home.html")

@app.route('/b2', methods=['POST',])
def b2() :
	send_message(0)
	return render_template("home.html")

if __name__ == "__main__" :
	app.run(host="127.0.0.1",port=5000)