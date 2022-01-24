#!/usr/bin/env python3
# @author   Markus Kösters

import socket
from HardwareConfiguration.ConfigReader import ConfigReader
import sys


class Server:
    
    def __init__(self):
        self.__conf = ConfigReader()
        self.__HOST = self.__conf.readConfigParameter('Socket_IP_Address')
        self.__PORT = self.__conf.readConfigParameter('Socket_IP_Port')       # Port to listen to (non-privileged ports are > 1024)
        self.__socketServer = None
        self.__userInformed = False

    def setupServer(self):
        try:
            self.__connectionEstablished = False
            self.__socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__socketServer.bind((self.__HOST, self.__PORT))
            self.__socketServer.listen()
            self.__conn, self.__addr = self.__socketServer.accept()
            self.__connectionEstablished = True
        except:
            self.__connectionEstablished = False

    def sendData(self, data):
        __data = data
        __byteData = []
        if self.__connectionEstablished:
            try:
                for __element in __data:
                    try:
                        __byteData = (__element.to_bytes(1, byteorder=sys.byteorder))
                    except:
                        pass
                self.__conn.sendall(__byteData)
            except Exception as e:
                print(f'Error during data-transmission:  {e}')
        else:
            if not self.__userInformed:
                print('Connection NOT established try calling setupServer again!')
                self.__userInformed = True

    def closeServer(self):
        self.__socketServer.close()
        
