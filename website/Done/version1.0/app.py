from flask import Flask,render_template,request,Response,session,escape
from Database import Database
from jinja2 import Template
from tools import get_content,get_time,save_md

app = Flask(__name__)
Database = Database()
every_page_num = 5

@app.route('/',methods=['GET',])
def home() :
	pagenum = 1
	Database.connect()
	allblognum = Database.get_blog_number()
	if allblognum>=5 :
		side_article_info = Database.get_blog_for_side(1, 5)
	else :
		side_article_info = Database.get_blog_for_side(1, allblognum)
	mp = int((allblognum+every_page_num+1)/every_page_num)
	articles = Database.get_many_blog(allblognum-every_page_num*pagenum+1,allblognum-every_page_num*(pagenum-1))
	articles = articles[-1::-1]
	Database.close()
	if 'user' in session and not escape(session['user'])=='stranger' :
		return render_template('homepage.html',user=escape(session['user']),articles=articles, pagenum=pagenum,allnum=mp,side_article_info=side_article_info)
	else :
		session['user'] = 'stranger'
		session['password'] = '12345'
		return render_template('homepage.html',user='stranger',articles=articles, pagenum=pagenum,allnum=mp,side_article_info=side_article_info)

@app.route('/home/<int:pagenum>')
def page(pagenum) :
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
	return render_template('homepage.html', articles=articles, pagenum=pagenum,allnum=mp,user=escape(session['user']),side_article_info=side_article_info)





@app.route("/code-editor",methods=['GET'])
def code() :
	if 'user' in session and not escape(session['user'])=='stranger' :
		return render_template('code_editor.html', user=escape(session['user']))
	else :
		return render_template('code_editor.html', user='stranger')

@app.route("/save_code",methods=['POST',])
def save_code() :
	if 'user' in session and not escape(session['user'])=='stranger' :
		print(request.form)
		return render_template('code_editor.html', user=escape(session['user']))
	else :
		return render_template('code_editor.html', user='stranger')

@app.route('/md-editor/edit')
def md() :
	if 'user' in session and not escape(session['user'])=='stranger' :
		return render_template('md_editor_edit.html', user=escape(session['user']))
	else :
		return render_template('md_editor_edit.html', user='stranger')

@app.route('/md-editor/show/<int:blogid>')
def md_show(blogid) :
	return render_template('md_editor_show.html',blogid=blogid)

@app.route('/md/<int:blogid>',methods=['GET','POST'])
def getmd(blogid) :
	Database.connect()
	path = Database.get_blog(blogid)
	Database.close()
	with open(path,'rb') as fi :
		rep = fi.read()
	return Response(rep,mimetype='text/markdown')

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
								<input type="button" class='side-form-button' id="login-button" value='提交'/>
							</form>
	'''
	user = request.form['user']
	password = request.form['password']
	try :
		Database.connect()
		if Database.check_user(user, password) :
			session['user'] = user
			session['password'] = password
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
								<input type="button" class='side-form-button' id="login-button" value='提交'/>
							</form>
	'''
	session['user'] = 'stranger'
	session['password'] = '12345'
	template = Template(fail_message)
	return template.render(user='stranger')

@app.route('/save-blog', methods=['POST',])
def save_blog() :
	if 'user' in session and not escape(session['user'])=='stranger' :
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
		return render_template('md_editor_edit.html', user='stranger')

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
	try :
		Database.connect()
		if 'user' in session and Database.check_user(escape(session['user']), escape(session['password']))==1 :
			user = Database.show_all_user(not_print=True)
			blog = Database.show_all_blog(not_print=True)
			return render_template('root.html', user=user, blog=blog)
		else :
			return "没有权限"
	except Exception as err:
		print(err)
		Database.close()
	finally :
		Database.close()


app.secret_key = '123abc'

if __name__ == '__main__' :
	try :
		app.run(host="0.0.0.0",debug=True,port=8000)
	except :
		pass