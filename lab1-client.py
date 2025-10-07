import socket
import threading
import sys 

ip_port=('10.128.0.2', 9999)

#function to display incoming messages to the client without requiring client input
def recieve_message(sock):
    while True:
        try:
            data = sock.recv(1024).decode()
            if not data:
                break
            #Manages the output such that input command comes after the recieved server message
            sys.stdout.write("\r" + " " * 80 + "\r")  
            print(f"\n{data}")
            sys.stdout.write("input command: ")
            sys.stdout.flush()
        except:
            break

s = socket.socket()
s.connect(ip_port)

#Client recieves ID and displays it upon connection
client_id = s.recv(1024).decode()
print(client_id)

#thread to run the recieving messages function
threading.Thread(target=recieve_message, args=(s,), daemon=True).start()


#while True:
#    inp = input('input command： ').strip()
#    if not inp:
#        continue
#    s.sendall(inp.encode())
#
#    if inp == "exit":
#        print("communication end！")
#        break

s.close()