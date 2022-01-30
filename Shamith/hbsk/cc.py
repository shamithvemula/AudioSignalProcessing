#!/usr/bin/env python3
import socket
from socket import AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET, SHUT_RDWR
from logging import addLevelName
import string
import random
from random import randint
import ssl
from iec62056_21.client import Iec6205621Client



#--------------------------------------------------------------#
#import the libraries needed for client
#--------------------------------------------------------------#

HOST =  'shamith'   #'172.17.0.2'

PORT = 8081

address = (HOST, PORT)  

#--------------------------------------------------------------------#
#initialising protocol TLS
#--------------------------------------------------------------------#

server_sni_hostname = 'reDesigN'
server_cert = 'server.crt'
client_cert = 'client.crt'
client_key = 'client.key'

#context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile='/home/shamith/Desktop/Project/Server/server.crt')
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2) #cafile='/home/shamith/Desktop/Project/Server/server.crt')
#context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT, cafile='/home/shamith/Desktop/Project/Server/server.crt')

context.verify_mode = ssl.CERT_REQUIRED

context.load_cert_chain(certfile=client_cert, keyfile=client_key)

#context.load_verify_locations(cafile='/home/shamith/Desktop/Project/Server/server.crt')
context.load_verify_locations(cafile= server_cert)

  
#--------------------------------------------------------------#
#initializing random values in dictionary to take meter readings
#--------------------------------------------------------------#

def read_value(key):
    obis_iden = ['0.9.1', '1.8.0', '2.8.0', '3.8.0', '1.8.3', '2.2.0', '3.2.0', '1.8.1', '1.8.2', '1.8.3']
    i,j = 50, 250000
    result = {ele : randint(i, j) for ele in obis_iden}
    return result[key]
    
def int_generator(chars=range(0, 250000)):
    """Function to generate random integers with with specified size"""
    return random.choice(chars)

#-----------------------------------------------------------------------#
# Initialize Iec6205621Client instance with tcp
#-----------------------------------------------------------------------#

def run_client():
    
     client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
                          
     print("socket created")
     
     client_sock.connect(address)                  # Connect client to server
     
     print("connected with server successfully")
     
     print("Intiating to send the meter data")
     
     client = context.wrap_socket(client_sock, server_side=False, server_hostname=server_sni_hostname, do_handshake_on_connect=True, suppress_ragged_eofs=True, session=None)
     print("TLSv1_2 established. Peer: {}".format(client.getpeercert()))
     
     client.send(bytes('hello', 'utf -8'))
     
     '''with client:
         
         client = Iec6205621Client.with_tcp_transport(address=(HOST, PORT), device_address='12345678', password='00000000')
         
         number_of_data_to_send = 100
         sent_data = 0
         while(sent_data < number_of_data_to_send):
             
             data = int_generator()
             client.write_single_value(address=address, data=data)
             sent_data+=1
    
         data_1 = read_value('1.8.0')                 
     
         client.write_single_value(address=address, data=data_1)
         
         
         """
          Writes a value to an address in the device.

          :param address:
          :param data:
          :return:
        """
    '''
     
         
         
        
     client.shutdown(socket.SHUT_RDWR)     
     client_sock.close()
     
     print("client disconnected")
     


if __name__ == "__main__":
    run_client()     








