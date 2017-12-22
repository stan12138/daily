from flask import Flask,render_template,request,Response,session,escape,redirect,url_for
from Database import Database
from jinja2 import Template
from tools import get_content,get_time,save_md
import time

app = Flask(__name__)
Database = Database()
every_page_num = 5
remember_login_time = 3600

@app.route('/',methods=['GET',])
def home() :
	pagenum = 1
	Database.connect()
	allblognum = Database.get_blog_number()
	if allblognum>=5 :
		side_article_info = Database.get_blog_for_side(1, 5)
	else :
		side_article_info = Database.get_blog_for_side(1, allblognum)
	mp = int(allblognum/every_page_num)+1
	articles = Database.get_many_blog(allblognum-every_page_num*pagenum+1,allblognum-every_page_num*(pagenum-1))
	articles = articles[-1::-1]
	Database.close()

	user = "stranger"
	if "time" in session and time.time()-int(escape(session['time'])) < remember_login_time:
		user = escape(session['user'])
		return render_template('homepage.html',user=user,articles=articles, pagenum=pagenum,allnum=mp,side_article_info=side_article_info)
	else :
		session['user'] = 'stranger'
		session['password'] = '12345'
		return render_template('homepage.html',user='stranger',articles=articles, pagenum=pagenum,allnum=mp,side_article_info=side_article_info)

@app.route('/home/<int:pagenum>')
def page_n(pagenum) :
	Database.connect()
	allblognum = Database.get_blog_number()
	if allblognum>=5 :
		side_article_info = Database.get_blog_for_side(1, 5)
	else :
		side_article_info = Database.get_blog_for_side(1, allblognum)
	mp = int((allblognum+every_page_num+1)/every_page_num)
	if pagenum<1 :
		pagenum = 1
	elif pagenum>mp :
		pagenum = mp

	if pagenum<mp :
		articles = Database.get_many_blog(allblognum-every_page_num*pagenum+1,allblognum-every_page_num*(pagenum-1))
	else :
		articles = Database.get_many_blog(1,allblognum-every_page_num*(pagenum-1))
	Database.close()

	articles = articles[-1::-1]

	user = "stranger"
	if 'user' in session :
		user = escape(session['user'])
	
	return render_template('homepage.html', articles=articles, pagenum=pagenum,allnum=mp,user=user,side_article_info=side_article_info)




@app.route("/code-editor",methods=['GET'])
def code_editor() :
	user = "stranger"
	if "time" in session and time.time()-int(escape(session['time'])) < remember_login_time:
		user = escape(session['user'])
		return render_template('code_editor.html', user=user)
	else :
		session['user'] = 'stranger'
		session['password'] = '12345'
		return render_template('code_editor.html', user='stranger')

@app.route("/save_code",methods=['POST',])
def save_code() :
	Database.connect()
	user = "stranger"
	if "time" in session and time.time()-int(escape(session['time'])) < remember_login_time:
		user = escape(session['user'])
		authority = Database.check_user(user, password="12345",name_only=True)
		Database.close()
		if authority==1 :
			print(request.form)
			return render_template('code_editor.html', user=user, flash_messages=[('success', '代码提交成功'),])
		else :
			return render_template('code_editor.html', user=user, flash_messages=[('danger', '没有权限'),])
	else :
		session['user'] = 'stranger'
		session['password'] = '12345'
		return render_template('code_editor.html', user=user, flash_messages=[('danger', '没有权限'),])




@app.route('/md-editor/show/<int:blogid>')
def md_show(blogid) :
	if "time" in session and time.time()-int(escape(session['time'])) < remember_login_time:
		user = escape(session["user"])
		password = escape(session["password"])
		Database.connect()
		auth = Database.check_blog_haver(blogid)
		authority = Database.check_user(user, password)
		Database.close()
	else :
		session['user'] = 'stranger'
		session['password'] = '12345'
		user = 'stranger'
		auth = 'xxxxx'
		authority = '2'
	return render_template('md_editor_show.html',blogid=blogid,user=user,authority=authority,auth=auth)

@app.route('/md-editor/edit')
def md_edit() :
	if "time" in session and time.time()-int(escape(session['time'])) < remember_login_time:
		return render_template('md_editor_edit.html', user=escape(session['user']))
	else :
		session['user'] = 'stranger'
		session['password'] = '12345'
		return render_template('md_editor_edit.html', user='stranger')

@app.route("/reedit",methods=["POST",])
def md_reedit() :
	Database.connect()
	blogid = request.form['blogid']
	auth = Database.check_blog_haver(blogid)
	if "time" in session and time.time()-int(escape(session['time'])) < remember_login_time:
		user = escape(session['user'])
	else :
		session['user'] = 'stranger'
		session['password'] = '12345'
		user = 'stranger'
	authority = Database.check_user(user, password='12345', name_only=True)
	path = Database.get_blog(blogid)
	Database.close()

	if auth==user or authority==1 :
		with open(path,'rb') as fi :
			content = fi.read()
		return render_template("md_editor_edit_again.html",md_content=content.decode('utf-8'),user=user,blogid=blogid)
	else :
		redirect('/md-editor/show/'+blogid)

@app.route("/reddit_save_blog",methods=['POST',])
def reddit_save_blog() :
	Database.connect()
	blogid = request.form['blogid']
	content = request.form['content']
	auth = Database.check_blog_haver(blogid)
	if "time" in session and time.time()-int(escape(session['time'])) < remember_login_time:
		user = escape(session['user'])
	else :
		session['user'] = 'stranger'
		session['password'] = '12345'
		user = 'stranger'
	authority = Database.check_user(user, password='12345', name_only=True)
	path = Database.get_blog(blogid)
	if auth==user or authority==1 :
		with open(path,'wb') as fi :
			fi.write(content.encode('utf-8'))
		date = get_time()
		c = get_content(content)
		Database.change_blog(blogid, c, date)

	Database.close()
	return redirect('/md-editor/show/'+blogid)

@app.route('/md/<int:blogid>',methods=['GET','POST'])
def get_md(blogid) :
	Database.connect()
	path = Database.get_blog(blogid)
	Database.close()
	with open(path,'rb') as fi :
		rep = fi.read()
	return Response(rep,mimetype='text/markdown')

@app.route('/save-blog', methods=['POST',])
def save_blog() :
	if 'user' in session and not escape(session['user'])=='stranger' :
		if time.time()-int(escape(session['time'])) < remember_login_time :
			content = request.form['content']
			title = request.form['title']
			user = escape(session['user'])
			c = get_content(content)
			now = get_time()
			path = save_md(content, user)
			Database.connect()
			Database.add_blog(title=title, auth=user, create_date=now, content=c, path=path)
			Database.close()
			return render_template('md_editor_edit.html', user=escape(session['user']))
		else :
			session['user'] = 'stranger'
			session['password'] = '12345'
			return render_template('md_editor_edit.html', user=escape(session['user']))
	else :
		return render_template('md_editor_edit.html', user='stranger')

@app.route('/login', methods=['POST',])
def login() :
	success_message = '''
	<h4>Login State</h4>
	{% for message in flash_messages %}
        <div class="alert alert-{{ message[0] }}">
        	<button type="button" class="close" data-dismiss="alert">&times;</button>
        	{{ message[1] }}
        </div>
    {% endfor %}
	<div id='state'>Hello, {{ user }}</div>
	<br/>
	<input type='button' class='side-form-button' id='logout-button' value='退出'/>'''
	fail_message = '''
							<h4>Login State</h4>
							{% for message in flash_messages %}
	                            <div class="alert alert-{{ message[0] }}">
	                            	<button type="button" class="close" data-dismiss="alert">&times;</button>
	                            	{{ message[1] }}
	                            </div>
	                        {% endfor %}							
							<div id="state">Hello, {{ user }}</div>
							<form method="post" id="login-form">
								<h4>Login in</h4>
								<p class="form-text">User name</p>
								<p><input class="side-form form-box" type="text" name="user" id="user"></p>
								<p class="form-text">Password</p>
								<p><input class="side-form form-box" type="password" name="password" id="password"></p>
								<input type="button" class='side-form-button' id="login-button" value='登录'/>
	                            <input type="button" class='side-form-button' id="register-button" value='注册'/>
							</form>
	'''
	user = request.form['user']
	password = request.form['password']
	try :
		Database.connect()
		if Database.check_user(user, password) :
			session['user'] = user
			session['password'] = password
			session['time'] = int(time.time())
			template = Template(success_message)
			return template.render(user=user, flash_messages=[('success', '登陆成功，%s'%user)])
		else :
			session['user'] = 'stranger'
			session['password'] = '12345'
			template = Template(fail_message)
			return template.render(user='stranger', flash_messages=[('danger', '用户不存在'),])
	except :
		Database.close()
	finally :
		Database.close()
@app.route('/logout', methods=['GET',])
def logout() :
	fail_message = '''
							<h4>Login State</h4>
							{% for message in flash_messages %}
	                            <div class="alert alert-{{ message[0] }}">
	                            	<button type="button" class="close" data-dismiss="alert">&times;</button>
	                            	{{ message[1] }}
	                            </div>
	                        {% endfor %}							
							<div id="state">Hello, {{ user }}</div>
							<form method="post" id="login-form">
								<h4>Login in</h4>
								<p class="form-text">User name</p>
								<p><input class="side-form form-box" type="text" name="user" id="user"></p>
								<p class="form-text">Password</p>
								<p><input class="side-form form-box" type="password" name="password" id="password"></p>
								<input type="button" class='side-form-button' id="login-button" value='登录'/>
	                            <input type="button" class='side-form-button' id="register-button" value='注册'/>
							</form>
	'''
	session['user'] = 'stranger'
	session['password'] = '12345'
	template = Template(fail_message)
	return template.render(user='stranger')

@app.errorhandler(404)
def page(e) :
	return render_template('wrong.html')

@app.route("/favicon.ico")
def icon() :
	with open("static/images/stan.ico",'rb') as fi :
		rep = fi.read()
	return Response(rep,mimetype='image/x-icon')

@app.route("/root")
def root() :
	Database.connect()
	if 'user' in session and Database.check_user(escape(session['user']), escape(session['password']))==1 :
		if time.time()-int(escape(session['time'])) < remember_login_time :
			user = Database.show_all_user(not_print=True)
			user_num = len(user)
			blog = Database.show_all_blog(not_print=True)
			Database.close()
			return render_template('root.html', user=zip(user,range(user_num)), blog=blog)
		else :
			Database.close()
			session['user'] = 'stranger'
			session['password'] = '12345'
			return "没有权限"
	else :
		Database.close()
		return "没有权限"
	

@app.route("/delete_user",methods=["POST",])
def delete_user() :
	Database.connect()
	if 'user' in session and Database.check_user(escape(session['user']), escape(session['password']))==1 :
		user = request.form['user']
		Database.delete_user(user)
		Database.close()
		return redirect("/root")

	else :
		return "没有权限"

@app.route("/change_password",methods=["POST",])
def change_password() :
	Database.connect()
	if 'user' in session and Database.check_user(escape(session['user']), escape(session['password']))==1 :
		user = request.form['user']
		password = request.form['password']
		Database.change_user_password(user, password)
		Database.close()
		return redirect("/root")

	else :
		return "没有权限"

@app.route("/change_authority",methods=["POST",])
def change_authority() :
	Database.connect()
	if 'user' in session and Database.check_user(escape(session['user']), escape(session['password']))==1 :
		user = request.form['user']
		authority = request.form['authority']
		Database.change_user_authority(user, authority)
		Database.close()
		return redirect("/root")

	else :
		return "没有权限"

@app.route("/delete_blog",methods=["POST",])
def delete_blog() :
	Database.connect()
	if 'user' in session and Database.check_user(escape(session['user']), escape(session['password']))==1 :
		blog_id = request.form['id']
		Database.delete_blog(int(blog_id))
		Database.close()
		return redirect("/root")

	else :
		return "没有权限"



@app.route("/register",methods=['POST',])
def register() :
	success_message = '''
	<h4>Login State</h4>
	{% for message in flash_messages %}
        <div class="alert alert-{{ message[0] }}">
        	<button type="button" class="close" data-dismiss="alert">&times;</button>
        	{{ message[1] }}
        </div>
    {% endfor %}
	<div id='state'>Hello, {{ user }}</div>
	<br/>
	<input type='button' class='side-form-button' id='logout-button' value='退出'/>'''
	fail_message = '''
							<h4>Login State</h4>
							{% for message in flash_messages %}
	                            <div class="alert alert-{{ message[0] }}">
	                            	<button type="button" class="close" data-dismiss="alert">&times;</button>
	                            	{{ message[1] }}
	                            </div>
	                        {% endfor %}							
							<div id="state">Hello, {{ user }}</div>
							<form method="post" id="login-form">
								<h4>Login in</h4>
								<p class="form-text">User name</p>
								<p><input class="side-form form-box" type="text" name="user" id="user"></p>
								<p class="form-text">Password</p>
								<p><input class="side-form form-box" type="password" name="password" id="password"></p>
								<input type="button" class='side-form-button' id="login-button" value='登录'/>
	                            <input type="button" class='side-form-button' id="register-button" value='注册'/>
							</form>
	'''
	user = request.form['user']
	password = request.form['password']
	try :
		Database.connect()
		if Database.add_user(user, password) :
			session['user'] = user
			session['password'] = password
			session['time'] = int(time.time())
			template = Template(success_message)
			return template.render(user=user, flash_messages=[('success', '注册成功，%s'%user)])
		else :
			session['user'] = 'stranger'
			session['password'] = '12345'
			template = Template(fail_message)
			return template.render(user='stranger', flash_messages=[('danger', '用户名已存在'),])
	except Exception as er:
		print(er)
		Database.close()
	finally :
		Database.close()
app.secret_key = '123abc'

if __name__ == '__main__' :
	try :
		app.run(host="0.0.0.0",debug=True,port=8000)
	except :
		pass