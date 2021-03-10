# Version 0.0.0
# Developed by XM
# (C) 2021

import os
import socket
#from socket import socket
import socks
import select
import sys
import requests
from requests import get
import threading
# Chat stuff
import datetime
import time
import random
from random import randint
# Proxy stuff
from stem import Signal
from stem.control import Controller
from colorama import init

GREEN =  '\033[32;1m' # Green Text
END = '\033[m' # reset to the defaults
SYSMS = "\033[32;1m[SYSTEM]: \033[m"
INPMS = "\033[35;1m[USER]: \033[m"
DEBUG = "\033[31;1m[DEBUG]: \033[m"


HEADER_LENGTH = 10

host = "127.0.0.1"
port = 9012
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen()
sockets_list = [s]
clients = {}
print(SYSMS + f"Server is running @ {host}:{port}")
print(SYSMS + "Waiting for incoming connections...")



def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        if not len(message_header):
            return False
        message_length = int(message_header.decode('utf-8').strip())
        return {'header': message_header, 'data': client_socket.recv(message_length)}
    except:
        return False

while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    for notified_socket in read_sockets:
        if notified_socket == s:
            client_socket, client_address = s.accept()
            user = receive_message(client_socket)
            if user is False:
                continue
            sockets_list.append(client_socket)
            clients[client_socket] = user
            print(SYSMS + 'Accepted new connection at ' + str(client_address))
        else:
            message = receive_message(notified_socket)
            #print(DEBUG + str(message)) #debug
            if message is False:
                print(SYSMS + 'Closed a connection.')
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            user = clients[notified_socket]
            print(SYSMS + 'Received message from user.')
            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
