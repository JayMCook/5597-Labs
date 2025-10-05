import socket

ip_port=('10.128.0.2', 9999)

#function to display incoming messages to the client without requiring client input
def recieve_message(sock):
    while True:
        try:
            data = sock.recv(1024).decode()
            if not data:
                break
            print(f"\n{data}") 
        except:
            break

s = socket.socket()
s.connect(ip_port)

#Client recieves ID and displays it upon connection
client_id = s.recv(1024).decode()
print(client_id)

#thread to run the recieving messages function
threading.Thread(target=recieve_message, args=(s,), daemon=True).start()

while True:
    inp = input('input command： ').strip()
    if not inp:
        continue
    s.sendall(inp.encode())

    if inp == "exit":
        print("communication end！")
        break

    server_reply = s.recv(1024).decode()
    print(server_reply)
s.close()