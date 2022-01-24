#!/usr/bin/env python3
# @author      Markus Kösters

import os

hardwareConfigDict = {}


class ConfigReader:

    def __init__(self):
        global hardwareConfigDict
        __dirPath = os.path.dirname(os.path.realpath(__file__))
        self.__confFile = os.path.join(__dirPath, 'Hardware.conf')

    def readConfig(self):
        """Reads Hardware.conf and returns it as dictionary."""
        global hardwareConfigDict
        if not hardwareConfigDict:
            self.__configList = {}
            with open(self.__confFile, 'r') as __file:
                for __line in __file:
                    __line = __line.strip()
                    if __line and not __line.startswith('#'):
                        if '#' in __line:
                            __line = (__line.split('#'))[0]
                        __configParameter, __configInfo = __line.split('=')
                        __configInfo = __configInfo.strip()
                        if __configInfo.startswith('='):
                            __configInfo = __configInfo[1:].strip()
                        self.__configList[str(__configParameter).strip()] = __configInfo
            hardwareConfigDict = self.__configList
        else:
            self.__configList = hardwareConfigDict
        return self.__configList

    def readConfigParameter(self, parameter):
        """Reads and returns a single Parameter of Hardware.conf"""
        self.readConfig()
        __parameter = parameter.strip()
        __configInfo = str(self.__configList.get(__parameter))
        if ',' in __configInfo:
            __configInfo = __configInfo.split(',')
            for i in range(len(__configInfo)):
                __configInfo[i] = __configInfo[i].strip()
        elif __configInfo == 'None':
            __configInfo = None
        else:
            __configInfo = str(__configInfo).strip()
        return __configInfo

#Testing
#Conf = ConfigReader()
#print(Conf.readConfigParameter('CameraDelay'))