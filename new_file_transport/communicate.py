import socket
import threading
import os.path
import sys
import time


class CommunicateServer :
	def __init__(self, partner) :

		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.bind(('', 63834))
		self.server.listen(5)

		self.recv_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.partner_address = partner

		self.send_try_connect = True
		self.recv_try_connect = True

		self.send_loop = True
		self.recv_loop = True

		self.send_connect = False
		self.recv_connect = False

		self.recv_size = 1024*32
	def server_run(self) :
		#try_connect = True

		while self.send_try_connect :
			client, client_address = self.server.accept()
			if client_address[0] == self.partner_address[0] :
				self.send_try_connect = False
				self.send_connect = True
				print("get client.....")
			self.send_server = client

		while self.send_loop :
			a = input(">> ")
			if a=='file' :
				file_name = 'Lec01_方程组的几何解释.mp4'
				file_size = os.path.getsize(file_name)
				times = int(file_size/self.recv_size)+1
				
				content = str(file_size)+'\r\n'+str(times)+'\r\n'+file_name
				head = bytes("file\r\n"+str(len(content))+'\r\n'+content, 'utf-8')
				self.send_server.send(head)
				time.sleep(1)
				#哇，找到了，找到了，当发送文件的时候，客户端解析头需要一小段时间，而服务端完全没有等待，直接就发送了，所以导致
				#始终会有大约4344字节的消息丢失，所以只需要延时一点就可以了
				read_length = 0
				with open(file_name, 'rb') as fi :
					for i in range(times) :
						try :
							data = fi.read(self.recv_size)
							#self.send_server.sendall(data)
							#这里是一个很神奇的错误点，无论是send还是sendall都无法保证数据完整送到，偏偏我接受了
							#send的返回值之后就可以保证了，实在是很奇怪，问题到底出在哪?
							read_length += self.send_server.send(data)
							print('\r'+str(i)+'    '+str(read_length), end='')
						except :
							pass
			elif a=='message' :
				a = input("content: ")
				data = bytes('message\r\n'+str(len(a))+'\r\n'+a, 'utf-8')
				self.send_server.send(data)
			else :
				self.shutdown()

	def client_run(self) :
		#try_connect = True
		while self.recv_try_connect:
			try :
				self.recv_server.connect(self.partner_address)
				self.recv_try_connect = False
				self.recv_connect = True

				self.recv_file = self.recv_server.makefile('rb')
				print("get server.....")
			except :
				self.recv_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		while self.recv_loop :
			#self.recv_file = self.recv_server.makefile('rb')
			content_type = self.recv_file.readline()
			content_type = content_type.decode('utf-8')
			content_type = content_type.rstrip('\r\n')
			

			content_length = self.recv_file.readline()
			content_length = content_length.decode('utf-8')
			content_length = int(content_length.rstrip('\r\n'))


			data = self.recv_file.read(content_length)
			#self.recv_file.close()
			data = self.parse_data(data, content_type)

			if content_type == 'message' :
				print(data)
			elif content_type == 'file' :
				file_size, times, filename = data
				length = 0
				print(file_size, filename)
				with open(filename,'wb') as fi :		#18.4.9 0:05 文件传输出现错误，无法读取足够长度的内容，未知错误出在何处，发送或者接受？
					for i in range(times*2) :
						data = self.recv_file.read(self.recv_size)
						length += len(data)
						fi.write(data)
						print('\r'+str(length), end='')
						if length >= file_size :
							break

			

	def shutdown(self) :
		self.send_try_connect = False
		self.send_loop = False
		self.recv_loop = False
		self.recv_try_connect = False
		try :
			self.recv_file.close()
		except :
			pass
		self.server.close()
		self.recv_server.close()
		try :
			self.send_server.close()
		except :
			pass
		sys.exit()
	def parse_data(self, data, content_type) :
		data = data.decode('utf-8')

		if content_type == 'message' :
			return data
		elif content_type == 'file' :
			data = data.split('\r\n')
			return int(data[0]), int(data[1]), data[2]


my_client = CommunicateServer(('10.210.68.195', 63834))

a1 = threading.Thread(target=my_client.server_run, daemon=False)
a2 = threading.Thread(target=my_client.client_run, daemon=True)

a1.start()
a2.start()

a1.join()
