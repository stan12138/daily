import select, socket
import os.path
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server.setblocking(False)
server.bind(('0.0.0.0',5000))

server.listen(10)

in_list = [server]
out_list = []
server_go = True
client_go = True

max_size = 1024*32

while server_go:
	client, client_address = server.accept()
	print("get connect from",client_address)

	while client_go:
		data = client.recv(1024)
		if data == b'ready' :
			file_size = os.path.getsize("moumoon.mp4")
			times = int(file_size/max_size)+1
			file_name = 'moumoon.mp4'

			client.send(bytes(str(file_size)+'\n'+str(times)+'\n'+file_name,'utf-8'))
		if data == b'get info' :
			with open(file_name,'rb') as fi :
				for i in range(times) :
					try :
						data = fi.read(max_size)
						client.send(data)
						print('\r'+str(times-i-1),end='')
					except Exception as er:
						print(er)
						break
			if i==(times-1) :
				print("work done")
				client.close()
				server.close()
				client_go = False
				server_go = False
			else :
				print("fail")
				client.close()
				server.close()
				client_go = False
				server_go = False


'''

while in_list:
	
	read_list, write_list, error_list = select.select(in_list, out_list, in_list)

	
	for s in read_list :
		if s is server :
			client, client_address = s.accept()
			print("get connect from",client_address)
			client.setblocking(False)
			in_list.append(client)

		else :
			data = s.recv(1024)
			if data == b'ready' :
				file_size = os.path.getsize("moumoon.mp4")
				times = int(file_size/1024)+1
				file_name = 'moumoon.mp4'

				s.send(bytes(str(times)+'\n'+file_name,'utf-8'))
			if data == b'get info' :
				with open(file_name,'rb') as fi :
					for i in range(times) :
						data = fi.read(1024)
						s.send(data)
						if s.recv(1024) == b'1' :
							print('\r',times-i-1)
						else :
							break
				if i==(times-1) :
					print("work done")
					s.close()
					server.close()
					in_list = []
				else :
					print("fail")
					s.close()
					server.close()
					in_list = []
'''