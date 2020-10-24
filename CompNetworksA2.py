import socket
import sys
import os
import time
import random
import threading

from jobcreator import JobCreatorNode


#creates new client and excecutes tasks obtained from server
def client_node(server_address):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("Connecting {0} to {1}".format(client_socket, server_address))
    client_socket.connect(server_address)
    
    keep_connection = True

    while keep_connection:
        job = (client_socket.recv(1024)).decode()
        
        response = "COMPLETED {0}".format(job)
        if (random.randint(1,4) == 1):
            response = "REJECT"
        
        if (job == "AGAIN"):
            if (random.randint(1,4) == 1):
                response = "NO"
                keep_connection = False
            else:
                response = "YES"
        
        client_socket.send(response.encode())

    client_socket.close()
 
 #end client_node()




print("Runs properly")