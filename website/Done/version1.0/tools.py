import time

__all__ =['get_time', 'get_content', 'save_md','fail_message','success_message']


def get_time() :
	return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

def get_content(content) :
	a = content.split("\r\n")
	for i in a :
		if len(i)>=1 and not i[0]=='#' :
			return i
	return ''

def save_md(content,user) :
	filename = 'md/'+user+str(int(time.time()))+'.md'
	with open(filename,'wb') as fi :
		fi.write(content.encode('utf-8'))
	return filename

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
								<input type="button" class="side-form-button" id="login-button" value="登录"/>
								<input type="button" class="side-form-button" id="register-button" value="注册"/>
							</form>
	'''

success_message = '''
	<h4>Login State</h4>
	{% for message in flash_messages %}
        <div class="alert alert-{{ message[0] }}">
        	<button type="button" class="close" data-dismiss="alert">&times;</button>
        	{{ message[1] }}
        </div>
    {% endfor %}
	<div id="state">Hello, {{ user }}</div>
	<br/>
	<input type="button" class="side-form-button" id="logout-button" value="退出"/>'''

