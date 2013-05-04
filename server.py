# Import socket and thread management
import socket
import threading

# our ip address
ip = "127.0.0.1"
# incoming connection port
port = 9000
# message size. can be reduced to speed it up.
buffer_size = 1024

# creates a new socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind our ip and port to the new socket
sock.bind((ip, port))
# start listening to the socket
sock.listen(1)
print("Listening on ", ip, ":", port)

# an array of clients (sockets). Stores dictionaries containing
# { 'connection': connection, 'address': address, 'messages': list, 'active': bool }
clients = []

# send a message to all clients
def printMessage(account, data):
    for client in clients:
        if client['active'] == False:
            continue
        
        # if the client connection in the loop is equal to current connection, skip. We don't send it to the same connection.
        c_ip, c_port = client['address']
        a_ip, a_port = account['address']
        
        if c_ip == a_ip and c_port == a_port:
            continue
        
        # send the bytes
        msg = a_ip+":"+str(a_port)+" "+data;
        client['connection'].send(bytes(msg, "utf-8"))

# function to handle a single connection.
def handleClient(account):
    while True:
        # blocks the thread until some data is received.
        data = account['connection'].recv(buffer_size)
        
        # if data contains nothing or is false
        if not data:
            break
        
        decoded = data.decode('utf8').replace("\n", "")
        
        a_ip, a_port = account['address']
        
        # print what we received
        print(a_ip, ":", a_port, " sent \"", decoded, "\"")
        
        # if client wants to quit
        if decoded == "/exit":
            account['active'] = False
            
            break;
        elif decoded == "/list":
            msg = "Listing clients:\n"
            for client in clients:
                if client['active'] == False:
                    continue
                
                c_ip, c_port = client['address']
                msg = msg + "- Client on "+c_ip+":"+str(c_port)+"\n"
            
            account['connection'].send(bytes(msg, "utf-8"));
            continue
        elif decoded == "/log":
            msg = "Listing your messages:\n"
            for message in account['messages']:
                msg = msg + message + "\n"
            
            account['connection'].send(bytes(msg, "utf-8"))
            continue
        else:
            account['messages'].append(decoded)
        
        # forward it to all clients.
        printMessage(account, decoded)
    
    # close the connection
    print("Closing connection")
    account['connection'].shutdown(socket.SHUT_RDWR)
    account['connection'].close()

while True:
    # accept the connection
    conn, address = sock.accept()
    account = { 'connection':conn, 'address': address, 'messages': [], 'active': True };
    # add the new connection to the client list
    clients.append(account)
    
    print("New Connection address: ", address)
    #print(address)
    printMessage(account, "Connected.")
    
    # if the connection was looping here, it would be blocking this thread. Needs to start in its own thread.
    threading.Thread(target = handleClient, args=([account])).start()