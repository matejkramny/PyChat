from socket import *
import thread

HOST = 'localhost'
PORT = 21568
BUFSIZE = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)

def inputLoop():
    while True:
        u_in = raw_input("> ");
        if u_in:
            tcpCliSock.send(u_in+"\n");

def add(data):
    print data

def loop():
    while True:
        data = tcpCliSock.recv(BUFSIZE)
        if data:
            add(data);
thread.start_new_thread(loop, ());

inputLoop()