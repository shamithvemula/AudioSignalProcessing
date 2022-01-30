#!/usr/bin/env python3
import socket
from socket import AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET, SHUT_RDWR
from logging import addLevelName
import string
import random
from random import randint
import ssl
from iec62056_21.client import Iec6205621Client
from iec62056_21 import messages, constants, transports, exceptions





HOST =  'shamith'   #'172.17.0.2'

PORT = 8081

address = (HOST, PORT)  

def read_value(key):
    obis_iden = ['0.9.1', '1.8.0', '2.8.0', '3.8.0', '1.8.3', '2.2.0', '3.2.0', '1.8.1', '1.8.2', '1.8.3']
    i,j = 50, 250000
    result = {ele : randint(i, j) for ele in obis_iden}
    return result[key]
    
def int_generator(chars=range(0, 250000)):
    """Function to generate random integers with with specified size"""
    return random.choice(chars)

def run_client():
    
    client = Iec6205621Client.with_tcp_transport(address=(HOST, PORT), device_address='12345678', password='00000000')
    client.connect()
    
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



    print("client disconnected")
        


if __name__ == "__main__":
    run_client()     