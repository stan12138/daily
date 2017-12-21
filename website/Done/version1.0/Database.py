import sqlite3
import os


__all__ = ['Database',]


class Database :
	def __init__(self) :
		'''
		只有一个数据库，名为data.db，初始化程序会自动检查是否存在，如果不存在，会自动建立相应的文件夹，建立数据库文件
		建立两个表格，分别是user和blog，并完成表格的初始化。
		'''
		self.database_name = 'database/data.db'
	
		l1 = '''create table user(
			name text primary key,
			password text,
			authority int
			);'''
		l2 = '''create table blog(
			id int primary key,
			title text,
			auth text,
			create_date text,
			content text,
			path text,
			num int
			);'''

		file = os.listdir()
		if 'database' in file :
			pass
		else :
			os.mkdir('database')
		file = os.listdir('database')
		if 'data.db' in file :
			pass
		else :
			self.database = sqlite3.connect(self.database_name)
			
			self.database.execute(l1)
			self.database.execute(l2)
			
			self.database.execute('insert into user values("stan","112358",1);')
			#用户权限分为1和2，1是最高权限，2是普通权限
			self.database.commit()
			self.close()
	
	def connect(self) :
		#首先必须要先连接数据库
		self.database = sqlite3.connect(self.database_name)
		
	def close(self) :
		#最后必须关闭连接
		self.database.close()

	def show_all_user(self,not_print=False) :
		a = list(self.database.execute('select * from user;'))
		if not not_print :
			for i in a :
				print('user name:',i[0],'; password:',i[1],'; authority:',i[2])
		return a
	def add_user(self, name, password, authority=2) :
		if self.check_user(name, password, name_only=True) :
			return False
		else :
			self.database.execute('insert into user values("%s", "%s", %s);'%(name, password, authority))
			self.database.commit()
			return True

	def delete_user(self, name) :
		self.database.execute("delete from user where name='%s';"%name)
		self.database.commit()

	def change_user_password(self, name, password) :
		self.database.execute("update user set password='%s' where name='%s';"%(password,name))
		self.database.commit()

	def change_user_authority(self,name,authority) :
		self.database.execute("update user set authority='%s' where name='%s';"%(authority,name))
		self.database.commit()

	def check_user(self, name, password, name_only=False) :
		res = list(self.database.execute('select * from user where name="%s";'%name))
		get = False
		if name_only :
			for i in res :
				if name==i[0] :
					get = i[2]
					break
		else :
			for i in res :
				if name==i[0] and password == i[1] :
					get = i[2]
					break

		return get

	def add_blog(self, title, auth, create_date, content, path) :
		res = list(self.database.execute("select num from blog limit 1;"))
		num = 0
		if len(res) :
			num = res[0][0]
		blog_id = num + 1
		self.database.execute("insert into blog values (%s, '%s', '%s', '%s', '%s', '%s', %s);"%(blog_id,title,auth,create_date,content,path,num))
		self.database.execute("update blog set num=num+1;")
		self.database.commit()

	def show_all_blog(self,not_print=False) :
		res = list(self.database.execute("select * from blog;"))
		if not not_print :
			for i in res :
				for j in i :
					print(j)
		return res
	def delete_blog(self, blog_id) :
		res = list(self.database.execute("select num from blog limit 1;"))
		num = 0
		if len(res) :
			num = res[0][0]
		if blog_id<=num and num :
			self.database.execute("delete from blog where id=%s;"%blog_id)
			self.database.execute("update blog set id=id-1 where id>%s;"%blog_id)
			self.database.execute("update blog set num = num-1;")
			self.database.commit()
		return num-1
	def get_blog(self, blog_id) :
		path = False
		res = list(self.database.execute("select id, path from blog where id=%s;"%blog_id))
		for i in res :
			if i[0] :
				path = i[1]
				break
		return path

	def change_blog(self, blog_id, content) :
		self.database.execute("update blog set content='%s' where id=%s;"%(content, blog_id))
		self.database.commit()

	def get_blog_number(self) :
		res = list(self.database.execute("select num from blog where id=1;"))
		return res[0][0]

	def get_many_blog(self,id1,id2) :
		res = list(self.database.execute("select title, auth, create_date, content, id from blog where id>=%s AND id<=%s;"%(id1,id2)))
		return res

	def get_blog_for_side(self,id1,id2) :
		res = list(self.database.execute("select title, id from blog where id>=%s AND id<=%s;"%(id1,id2)))
		return res

if __name__ == '__main__' :
	try :
		db = Database()
		db.connect()
		db.show_all_user()

		print(db.add_user("s1", "12345"))
		print(db.add_user("stan", "12345"))
		db.show_all_user()
		db.delete_user("s1")
		db.show_all_user()
		print(db.check_user("stan", "1"))
		db.add_blog(title='12', auth='12', create_date='12', content='12', path='12')
		db.add_blog(title='13', auth='12', create_date='12', content='12', path='12')
		db.show_all_blog()
		db.delete_blog(1)
		db.show_all_blog()
		print(db.get_blog(1))
		print(db.get_blog('1'))
		print(db.get_blog(2))
		while db.delete_blog(1) :
			pass
		print("this is all blog")
		db.show_all_blog()
		db.close()
	except Exception as err:
		print(err)
		db.close()