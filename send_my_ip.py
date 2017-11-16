import socket
import smtplib
from email.mime.text import MIMEText
import requests
import time

def getIP() :
	s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	try :
		s.connect(("baidu.com",12567))
		ip = s.getsockname()[0]
		s.close()
	except Exception :
		ip = "N/A"

	return ip

def test_login(se) :
	content = se.get("http://baidu.com",timeout=1)
	if "baidu" in content.text :
		return True
	else :
		return False

def login(se) :
	postd = {"DDDDD":"2013212846",
	         "upass":"H31a41n",
	         "0MKKey":""}

	login_url = "http://10.3.8.211/"

	data = sen.post(login_url,postd)

def send_email(ip) :
	user = "2283295323@qq.com"
	code = "idxbxfcaspfbdjbf"

	reciver = "nats12138@163.com"

	msg = MIMEText("My IP is "+ip)
	msg["Subject"] = "this is my ip"
	msg["From"] = user
	msg["To"] = reciver

	try :
		smtp = smtplib.SMTP_SSL("smtp.qq.com")
		smtp.login(user, code)
		smtp.sendmail(user, reciver, msg.as_string())
		smtp.quit()
	except Exception :
		print("send fail...")	




time.sleep(20)
sen = requests.session()

if not test_login(sen) :
	login(sen)

ip = getIP()

send_email(ip)
