import socket
import sys
import threading
import os
import time
import random

# Job Creator Node - Makes a server node that connects to clients and interacts
# with them through protocols, and exchanges data.
class JobCreatorNode:
    
    JOB_TYPES = ["ICMP Request", "Craft and send IP packet", "Craft and send TCP packet", "Send HTTP GET request"]

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
            print("Server: Waiting for new connection...")
            self.node_socket.listen(1) #starts listening for connection
            
            connection, address = self.node_socket.accept() #connects to client
            self.total_clients += 1
            print("Server: Connected to client #{0}: {1}".format(self.total_clients, address))
            print("Server: Total clients: ", self.total_clients)
            client_id = int(connection.recv(1024).decode())

            new_thread = threading.Thread(target=self.communicate_with_client, args=(connection, address, client_id, ))
            new_thread.start()

    # Creates new thread to run communications between this server and specified client
    def communicate_with_client(self, connection, address, client_id):
        try:
            keep_connection = True
            while keep_connection:
                job = self.JOB_TYPES[random.randint(0, len(self.JOB_TYPES) - 1)]
                print("Server: Asking client {0} to do job - {1}".format(client_id, job))
                connection.sendall(job.encode())

                response = (connection.recv(1024)).decode()
                if (response == "REJECT"):
                    print("Server: Client {0} rejected job - {1}".format(client_id, job))
                    keep_connection = False
                    continue
                else:
                    print("Server: Client {0} successfully completed job - {1}".format(client_id, job))

                print("Server: Asking client {0} to perform job again...".format(client_id))
                connection.sendall("AGAIN".encode())
                response = (connection.recv(1024)).decode()

                if (response == "NO"):
                    keep_connection = False

                print("Server: Client {0}'s response to do job again: {1}".format(client_id, response))

            print("Server: Closing connection with client ", client_id)
            connection.close()
        except:
            print("Server: Closing connection with client ", client_id)

    def getAddress(self):
        return self.server_address