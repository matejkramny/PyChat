from socket import *
import threading
import sys

host = 'localhost'
port = 9000
buffer_size = 1024

sock = socket(AF_INET, SOCK_STREAM)
sock.connect((host, port))

print("Connected to ", host, ":", port)
print("Type and press enter to send a message.")
print("Type '/list' to show who is on the chat, '/log' to see your sent messages, /exit' to quit")

def inputLoop():
    while True:
        u_in = input("> ");
        if u_in:
            sock.send(bytes(u_in+"\n", "utf-8"));
            if u_in == "/exit":
                sys.exit(0) # closes this thread

def add(data):
    print (data.decode('utf-8'))

def loop():
    while True:
        data = sock.recv(buffer_size)
        
        # if no data then exit. Sign of socket shutdown
        if data == b'':
            break
        if data:
            add(data);

threading.Thread(target = loop).start()

inputLoop()