import socket
import select

#是否要持久化数据？数据库？文件？抑或不持久化，直接存入字典，或者列表。需要一个时间戳，以保证在线设备是最新的

#是不是应该采用OOP

class IP_Server :
	def __init__(self) :
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setblocking(False)
		self.server.bind(('0.0.0.0',6000))
		self.server.listen(10)

		self.r_list = [self.server]
		self.w_list = []

		#self.client = []

		self.device = {}

		self.ip_record = []
# 应该采用ID作为唯一的标识符，或者IP？
	def run(self) :
		while True:
			read_list, write_list, error_list = select.select(self.r_list, self.w_list, self.r_list)

			for s in read_list :
				if s is self.server :
					client, client_address = s.accept()
					if client_address[0] in self.ip_record :
						client.close()
					else :
						client.setblocking(False)
						self.r_list.append(client)
						#self.client.append(client)
						self.device[client] = [bytes(client_address[0], 'utf-8'),client_address[0],False]
						self.ip_record.append(client_address[0])
						print(client_address,'is on-line')
				else :
					data = s.recv(1024)
					if data.decode('utf-8') == 'off-line' :
						print(self.device[s],'is off-line')
						#self.client.remove(s)
						if s in self.device.keys() :
							self.ip_record.remove(self.device[s][1])
							del self.device[s]
						self.r_list.remove(s)
						s.close()
						self.tell_someone_offline()
					elif self.check_report(data) :
						#防止有人动手脚
						if not self.device[s][2] :
							self.device[s][0] = data + b'\n' + self.device[s][0]
							self.device[s][2] = True
						s.send(b'get')
						self.tell_other_device()
					else :
						if s in self.device.keys() :
							self.ip_record.remove(self.device[s][1])
							del self.device[s]
						self.r_list.remove(s)
						s.close()
						self.tell_someone_offline()


	def check_report(self,data) :
		data = data.decode('utf-8')
		data = data.split('\n')
		if len(data)==2 and len(data[0])<40 and len(data[1])<20 :
			return True
		else :
			return False

	def tell_other_device(self) :
		if len(self.ip_record) > 1 :
			print(self.ip_record)
			for client in self.device.keys() :
				message = b''
				for s in self.device.keys() :
					if not client is s :
						message += self.device[s][0] + b'\n\n'
				client.send(message)

	def tell_someone_offline(self) :
		for client in self.device.keys() :
			message = b''
			for s in self.device.keys() :
				if not client is s :
					message += self.device[s][0] + b'\n\n'
			if message == b'' :
				message = b'0'
			client.send(message)

Server = IP_Server()
Server.run()