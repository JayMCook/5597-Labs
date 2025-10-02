import socket

ip_port=('10.128.0.2', 9999)

s = socket.socket()
s.connect(ip_port)

#Client recieves ID and displays it upon connection
client_id = s.recv(1024).decode()
print(client_id)

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