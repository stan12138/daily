import socket
import threading

class Client :
	def __init__(self) :

		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.bind(('', 67834))
		self.server.listen(5)

		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.connect_ip = '10.210.68.210'

	def server_run(self) :
		connect_fail = True

		while connect_fail :
			client, client_address = self.server.accept()
			if client_address[0] == self.connect_ip :
				connect_fail = False

			self.server_client = client

		while True :
			a = input(">> ")
			if a=='stop' :
				self.server_client.close()
				self.server.close()
				self.client.close()
				break
			else :
				self.server_client.send(a.encode('utf-8'))

	def client_run(self) :
		connect_fail = True
		while connect_fail:
			try :
				self.client.connect((self.connect_ip, 67835))
				connect_fail = False
			except :
				pass
		while True :
			data = self.client.recv(1024)
			print(data)

my_client = Client()

a1 = threading.Thread(my_client.server_run, daemon=False)
a2 = threading.Thread(my_client.client_run, daemon=True)

a1.start()
a2.start()

a1.join()