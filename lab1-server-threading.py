import socket
import threading

def link_handler(link, client, id):
    print('server start to receiving msg from {id} ({client[0]}: {client[1]})....')
    while True:
        client_data = link.recv(1024).decode()
        if client_data == "exit":
            print('communication end with {id} ({client[0]}: {client[1]})....')
            break
        print('{id} ({client[0]}, {client[1]}) sent {client_data}....' )
        link.sendall('server had received your msg, {id}'.encode())
    link.close()

ip_port = ('0.0.0.0', 9999)
sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket.SOCK_STREAM is tcp
sk.bind(ip_port)
sk.listen(5)

print('start socket server，waiting client...')

while True:
    conn, address = sk.accept()

    client_id = str(random.randint(1000, 9999))

    print('create a new thread to receive msg from [%s:%s]' % (address[0], address[1]))
    t = threading.Thread(target=link_handler, args=(conn, address, client_id))
    t.start()