import time

__all__ =['get_time', 'get_content', 'save_md']


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
