from Database import Database
from tools import get_time,save_md

d = Database()
d.connect()

auth = "Stan"

for i in range(10) :
	c = "测试"+str(i)
	title = c
	create_date = get_time()
	path  =save_md(c, auth)
	d.add_blog(title, auth, create_date, c, path)
d.show_all_blog()
d.close()
