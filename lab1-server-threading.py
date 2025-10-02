import socket
import threading
import random

client_list = {}
lock = threading.Lock()

def link_handler(link, client, id):
    with lock:
        client_list[id] = client

    print(f'server start to receiving msg from {id} ({client[0]}: {client[1]})....')
    link.sendall(f'Your ID is: {id}')
    while True:
        client_data = link.recv(1024).decode()
        if client_data == "list":
            print(f'Active client IDs: {client_list}')
            continue
        if client_data == "exit":
            print(f'communication end with {id} ({client[0]}: {client[1]})....')
            break
        print(f'{id} ({client[0]}, {client[1]}) sent {client_data}....' )
        link.sendall(f'server had received your msg, {id}'.encode())
    link.close()
    with lock:
        if id in client_list:
            del client_list[id]

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