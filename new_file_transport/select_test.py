import select, socket, sys
from queue import Queue

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(False)

server.bind(('',5000))
server.listen(5)

input_list = [server]
output_list = []
message_list = {}

while input_list :
	read_list, write_list, error_list = select.select(input_list, output_list, input_list)

	for s in read_list :
		if s is server :
			client, client_address = s.accept()
			print("get connect from",client_address)
			client.setblocking(False)
			input_list.append(client)
			message_list[client] = Queue()

		else :
			data = s.recv(4096)
			if data :
				print("get message from",client_address, "content is :",data)
				message_list[s].put(data)
				if not s in output_list :
					output_list.append(s)
			else :
				if s in output_list :
					output_list.remove(s)
				input_list.remove(s)
				s.close()

				del message_list[s]

	for s in write_list :
		try :
			next_msg = message_list[s].get_nowait()
		except :
			output_list.remove(s)
		else :
			print("send",next_msg)
			s.send(next_msg)

	for s in error_list :
		input_list.remove(s)
		if s in output_list :
			output_list.remove(s)
		s.close()
		del message_list[s]