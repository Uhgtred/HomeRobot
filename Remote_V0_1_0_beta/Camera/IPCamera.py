#!/usr/bin/env python3
# @author   Markus Kösters

import cv2
from HardwareConfiguration.ConfigReader import ConfigReader


class IPCamera:
    
    def __init__(self):
        self.__conf = ConfigReader()
        self.__camera = self.__conf.readConfigParameter('CameraPath')
        self.__cameraDelay = self.__conf.readConfigParameter('CameraDelay')
        self.__cameraStream = cv2.VideoCapture(self.__camera)
    
    def readCamera(self):
        """Streams network-camera to a UI-Frame"""
        ret, frame = self.__cameraStream.read()
        cv2.imshow('RobotVision', frame)
        cv2.waitKey(self.__cameraDelay)
        
    def cleanCamera(self):
        """Releases camera and closes opened UI-Video-Frame"""
        self.__cameraStream.release()
        cv2.destroyAllWindows()
        
#cam=IPCamera()
#cam.readCamera()
