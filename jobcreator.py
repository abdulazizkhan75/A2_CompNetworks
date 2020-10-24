import socket
import sys
import threading
import os
import time
import random

# Job Creator Node - Makes a server node that connects to clients and interacts
# with them through protocols, and exchanges data.
class JobCreatorNode:
    
    JOB_TYPES = [""]


    # Defines the server node. Elements within node:
    #  node_socket - socket of this node
    #  server_address - address of this node's connection
    def __init__(self):
        self.server_ip = "localhost"
        self.port_num = 5555
        self.node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (self.server_ip, self.port_num)
        self.total_clients = 0
        self.started_server = False
        try:
            self.node_socket.bind(self.server_address)
            print("Created server {0} on port {1}".format(self.server_address[0], self.server_address[1]))
        except:
            print("Could not create server")

    # Starts server and sends intructions (jobs) to connected clients
    def startServer(self):
        if (self.started_server):
            pass

        self.started_server = True
        while self.started_server:
            print("Waiting for new connection...")
            self.node_socket.listen(1) #starts listening for connection
            
            connection, address = self.node_socket.accept() #connects to client
            print("Connected to client: ", address)
            self.total_clients += 1
            print("Total connected clients: ", self.total_clients)
            
            new_thread = threading.Thread(target=self.communicate_with_client, args=(connection, address, ))
            new_thread.start()

    # Creates new thread to run communications between this server and specified client
    def communicate_with_client(self, connection, address):
        keep_connection = True
        while keep_connection:
            job = self.JOB_TYPES[random.randint(0,self.JOB_TYPES.len()-1)]
            connection.send(job.encode())

            response = (connection.recv(1024)).decode()
            if (response == "REJECT"):
                print("Client {0} reject job {1}".format(address, job))
            else:
                print("Client {0} successfully completed job {1}".format(address, job))

            connection.send("AGAIN".encode())
            response = (connection.recv(1024)).decode()
            if (response == "NO"):
                keep_connection = False
        
        print("Closing connection with client ", address)
        self.total_clients -= 1
        connection.close()
