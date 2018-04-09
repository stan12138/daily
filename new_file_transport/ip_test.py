import socket
import threading

server_address = ('10.112.101.153',6000)

class IP_Handler :
	def __init__(self) :
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_address = server_address
		self.ID = 'Stan-Laptop'
		self.port = 67834
		
		self.device = []
	def connect(self) :
		try_connect = True
		while try_connect :
			try :
				self.client.connect(self.server_address)
				try_connect = False
			except :
				pass
	
	def report(self) :
		success = False
		while not success :
			self.client.send(bytes(self.ID+'\n'+str(self.port),'utf-8'))
			data = self.client.recv(1024)
			if data == b'get' :
				success = True
	def recv_ip(self) :
		while True :
			message = self.client.recv(4096)
			self.parse_ip_info(message)
	def parse_ip_info(self,message) :
		self.device = []
		
		message = message.decode('utf-8')
		if message == '0' :
			pass
		else :
			message = message.split('\n\n')
			#self.device = []
			for s in message :
				if s :
					s = s.split('\n')
					self.device.append((s[0],s[2],int(s[1])))
		print(self.device)
	
	def off_line(self) :
		self.client.send(b'off-line')
		self.client.close()
		
	def run(self) :
		try :
			self.connect()
			self.report()
			self.recv_ip()
		except :
			pass

def watch(client) :
	while not input() == 'stop' :
		pass
	client.off_line()


client = IP_Handler()

a1 = threading.Thread(target=watch, args=(client,), daemon=False)
a2 = threading.Thread(target=client.run, daemon=True)

a1.start()
a2.start()
a1.join()

