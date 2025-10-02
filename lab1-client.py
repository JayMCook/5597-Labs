import socket

ip_port=('10.128.0.2', 9999)

s = socket.socket()
s.connect(ip_port)

while True:
    inp = input('input msg： ').strip()
    if not inp:
        continue
    s.sendall(inp.encode())

    if inp == "exit":
        print("communication end！")
        break

    server_reply = s.recv(1024).decode()
    print(server_reply)
s.close()