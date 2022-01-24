#!/usr/bin/env python3
# @author   Markus Kösters

from HardwareConfiguration.ConfigReader import ConfigReader
import socket


class SocketClient:
    
    def __init__(self):
        self.__conf = ConfigReader()
        self.__serverConn = None
        self.__Host = self.__conf.readConfigParameter('Socket_IP_Address')
        self.__Port = self.__conf.readConfigParameter('Socket_IP_Port')
        self.__numberOfBytes = self.__conf.readConfigParameter('MaxReceivedBytes')
    
    def connect(self):
        try:
            self.__serverConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__serverConn.connect((self.__Host, self.__Port))
        except:
            pass
    
    def rcvCommands(self):
        try:
            if self.__serverConn is not None:
                __data = self.__serverConn.recv(self.__numberOfBytes)
                for i in range(len(__data)):
                    try:
                        __data[i] = __data[i].decode()
                    except:
                        pass
                return __data
        except:
            pass
        
    def disconnect(self):
        try:
            if self.__serverConn is not None:
                self.__serverConn.close()
        except:
            pass
