import socket
import sys
import os
import time
import threading
from jobcreator import JobCreatorNode
import random

def new_client(server_address, client_id):

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    #Connection between Client and Server
    print("Client {0}: Attempting to connect to {1}".format(client_id, server_address[0]))
    client_socket.connect(server_address)
    print("Client {0}: Successfully connected to server".format(client_id))
    
    #Assigns Client ID to the Client on the Server
    client_socket.sendall(str(client_id).encode())
    
    #Communication between Client
    try:
        keep_connection = True
        while keep_connection:
            job = (client_socket.recv(1024)).decode()
            print("Cleint {0}: Recieved job - {1}".format(client_id, job))
            
            #Reject or Accept Job
            response = "COMPLETED {0}".format(job)
            if (random.randint(1,4) == 1):
                response = "REJECT"
            
            print("Client {0}: {1}".format(client_id, response))
            client_socket.sendall(response.encode())
            
            #Server asking Client to do another Job
            job = (client_socket.recv(1024)).decode()
            print("Client {0}: Server asked to do another job".format(client_id))
            
            #Reject/Accept doing another Job
            if (random.randint(1,4) == 1):
                response = "NO"
                keep_connection = False
            else:
                response = "YES"
            
            print("Client {0}: Response - {1}".format(client_id, response))
            client_socket.sendall(response.encode())
        #Ending connection with Server
        print("Client {0}: Closing connection with server".format(client_id))
        client_socket.close()
    except:
        print("Client {0}: Closing connection with server".format(client_id))
        client_socket.close()

#end new_client


num_of_clients = int(input("How many clients? >"))

server_node = JobCreatorNode()

server_thread = threading.Thread(target=server_node.startServer, args=())
server_thread.start()

for i in range(0,num_of_clients):
    new_client_thread = threading.Thread(target=new_client, args=(server_node.getAddress(), i+1, ))
    new_client_thread.start()
