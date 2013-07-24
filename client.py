from socket import *
import threading
import sys

# Notes:
# checking for data in socket and asking for input from command line both blocks the main thread, thats why they need to run in separate threads.

# server ip address
host = '127.0.0.1'
# server port
port = 9000
buffer_size = 1024

# creates a new socket
sock = socket(AF_INET, SOCK_STREAM)
# connect to the server
sock.connect((host, port))

# Display help to the user
print("Connected to ", host, ":", port)
print("Type and press enter to send a message.")
print("Type '/list' to show who is on the chat, '/log' to see your sent messages, /exit' to quit")

# function running in this thread, polling for input from the command line
def inputLoop():
    while True:
        # ask for input, diplaying "> "
        u_in = input("> ");
        if u_in:
            # Send the input from the user to the server. Data must be sent in bytes
            sock.send(bytes(u_in+"\n", "utf-8"));
            # if user sent /exit we must quit thread here otherwise it will keep on polling for input and never quit
            if u_in == "/exit":
                # exit
                sys.exit(0) # closes this thread

# prints data
def add(data):
    print (data.decode('utf-8'))

# function running in another thread created by threading. This polls the socket for data
def loop():
    while True:
        # ask for data
        data = sock.recv(buffer_size)
        
        # if no data then exit. Sign of socket shutdown
        if data == b'':
            break
        if data:
            # print it to the console
            add(data);

# create a new thread target loop (to receive data from socket)
threading.Thread(target = loop).start()

# start polling for input
inputLoop()