#!/usr/bin/env python3
# @author   Markus Kösters

import threading
import time
from Controller.Controller import Controller
from HardwareConfiguration.ConfigReader import ConfigReader
from Network.SocketServer import Server
from Camera.IPCamera import IPCamera


class Main:
    
    def __init__(self):
        self.__conf = ConfigReader()
        self.__cont = Controller()
        self.__camera = IPCamera()
        self.__socketServer = Server()
        self.__socketServer.setupServer()
        self.__delay = float(self.__conf.readConfigParameter('DelayMain'))
        self.__cameraDelay = float(self.__conf.readConfigParameter('CameraDelay'))

        __controller = self.__cont.initController()
        print(__controller)
        self.__trackValues = []
        
        __controllerThread = threading.Thread(target=lambda: self.__cont.readController(__controller), name='ControllerThread')
        __controllerThread.daemon = True
        __controllerThread.start()
        
        __cameraThread = threading.Thread(target=self.__camReadContinuously, name='CameraThread')
        __cameraThread.daemon = True
        __cameraThread.start()
        
        # Need to start in separate processes probably Functions maybe have to be their own files for that
        __trackThread = threading.Thread(target=self.__sendTrackData, name='TrackThread')
        __trackThread.daemon = True
        __trackThread.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print('Program exit...')
        finally:
            self.exit_handler()
            
    def __camReadContinuously(self):
        while True:
            self.__camera.readCamera()

    def __sendTrackData(self):
        while True:
            self.__trackValues = self.__cont.getTrackValues()
            self.__socketServer.sendData(self.__trackValues)
            time.sleep(self.__delay)

    def exit_handler(self):
        self.__camera.cleanCamera()
        self.__socketServer.closeServer()


main = Main()
