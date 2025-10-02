import socket
import threading
import random

client_list = {}
lock = threading.Lock()

def link_handler(link, client, id):
    #thread lock acts as a key only one thread at a time can hold, and actions with lock will only 
    #happen when said thread has the lock. This way commands will not overlap when managing the global list
    #The dict contains the id as a key and the client object, to be used in the messaging functionality
    with lock:
        client_list[id] = link

    print(f'server start to receiving msg from {id} ({client[0]}: {client[1]})....')
    link.sendall(f'Your ID is: {id}. Command list: "list" - Displays a list of the active client IDs. "msg" followed by another client ID and a string - Will send the string along with your client ID to the client whos ID you entered. "exit" - Ends connection and removes client ID from client list.'.encode())
    while True:
        client_data = link.recv(1024).decode()
        #When client requests "list" the IDs are compiled from the client list and displayed to the client
        if client_data == "list":
            with lock:
                ids = ", ".join(client_list.keys())
            link.sendall(f'Active client IDs: {ids}'.encode())
            continue
        if client_data.startswith("msg "):
            _, recieve_id, message = client_data.split(" ", 2)
            with lock:
                    if target_id in client_list:
                        client_list[recieve_id].sendall(
                            f"Message from {id}: {message}".encode()
                        )
                        link.sendall(f"Sent to {recieve_id}".encode())
                    else:
                        link.sendall(f"Client {recieve_id} not found".encode())
            except ValueError:
                link.sendall(b"Usage: msg <id> <message>")
            continue
        if client_data == "exit":
            print(f'communication end with {id} ({client[0]}: {client[1]})....')
            link.sendall('Goodbye!'.encode())
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

print('start socket server, waiting client...')

while True:
    conn, address = sk.accept()
    client_id = str(random.randint(1000, 9999))
    print('create a new thread to receive msg from [%s:%s]' % (address[0], address[1]))
    t = threading.Thread(target=link_handler, args=(conn, address, client_id))
    t.start()