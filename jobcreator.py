import socket
import sys
import os
import time
import signal


# Job Creator Node - Makes a server node that connects to clients and interacts
#                    with them through protocols, and exchanges data.
class JobCreatorNode:
    
    # Defines the server node. Elements within node:
    #  name - name of server
    #  node_sock - socket of this node
    #  server_address - address of this node's connection
    #  process_id - (will be defined when server starts) process of child that runs server
    def __init__(self, name):
        self.name = name
        self.node_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (name, 10000)
        self.process_id = -1
        
        node_sock.bind(server_address)
        print >> sys.stderr, "Created server %s on port" % server_address
    
    # Starts server by forking child process to run connection, and returning child process 
    # id to parent process. Server will communicate with clients and send jobs to perform
    # while connection is active.
    def startServer():
        process_id = os.fork()
        
        if (process_id == 0):
            node_sock.listen(1) #starts listening for connection
            
            while True:
                connection, client_address = node_sock.accept() #connects to client
                
                try:
                    print >> sys.stderr, "% connected to %", name, client_address
                    time.sleep(5)
                
                finally:
                    connection.close()
            
            
        else:
            return process_id

    # Stops forked child process i.e. stops server from running
    def stopServer():
        os.kill(process_id, signnal.SIGKILL)
        
