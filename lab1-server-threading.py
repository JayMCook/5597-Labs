import socket
import threading
import random

client_list = {}
lock = threading.Lock()

def link_handler(link, client, id):
    #thread lock acts as a key only one thread at a time can hold, and actions with lock will only 
    #happen when said thread has the lock. This way commands will not overlap when managing the global list
    with lock:
        client_list[id] = client

    print(f'server start to receiving msg from {id} ({client[0]}: {client[1]})....')
    link.sendall(f'Your ID is: {id}'.encode())
    while True:
        client_data = link.recv(1024).decode()
        #When client requests "list" the IDs are compiled from the client list and displayed to the client
        if client_data == "list":
            with lock:
                ids = ", ".join(client_list.keys())
            link.sendall(f"Active client IDs: {ids}".encode())
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