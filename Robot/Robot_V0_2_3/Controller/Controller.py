#!/usr/bin/env python3
# @author   Markus Kösters

from evdev import InputDevice
import subprocess
import os
import time
from HardwareConfiguration.ConfigReader import ConfigReader


class Controller:

    def __init__(self):
        self.__conf = ConfigReader()
        self.__deviceVendor = self.__conf.readConfigParameter('DeviceVendorID')

        self.__LXAxis = self.__conf.readConfigParameter('LXAxis')
        self.__LYAxis = self.__conf.readConfigParameter('LYAxis')
        self.__LTrigger = self.__conf.readConfigParameter('LTrigger')
        self.__LBtn = self.__conf.readConfigParameter('LBtn')
        self.__L3 = self.__conf.readConfigParameter('L3')

        self.__RXAxis = self.__conf.readConfigParameter('RXAxis')
        self.__RYAxis = self.__conf.readConfigParameter('RYAxis')
        self.__RTrigger = self.__conf.readConfigParameter('RTrigger')
        self.__RBtn = self.__conf.readConfigParameter('RBtn')
        self.__R3 = self.__conf.readConfigParameter('R3')

        self.__StartBtn = self.__conf.readConfigParameter('StartBtn')
        self.__SelectBtn = self.__conf.readConfigParameter('SelectBtn')

        self.__ABtn = self.__conf.readConfigParameter('ABtn')
        self.__BBtn = self.__conf.readConfigParameter('BBtn')
        self.__XBtn = self.__conf.readConfigParameter('XBtn')
        self.__YBtn = self.__conf.readConfigParameter('YBtn')

        self.__XCross = self.__conf.readConfigParameter('XCross')
        self.__YCross = self.__conf.readConfigParameter('YCross')

    def initController(self):
        __controller = None
        try:
            __path = self.__conf.readConfigParameter('ControllerPath')
            __temp = subprocess.Popen(['ls', __path], stdout=subprocess.PIPE)

            __temp = __temp.communicate()
            __deviceList = (__temp[0]).decode()
            __deviceList = __deviceList.split('\n')

            for element in __deviceList:
                element = f'{__path}{element}'
                if 'event' in element:
                    if InputDevice(element).info.vendor == int(self.__deviceVendor):
                        __controller = InputDevice(element)
        finally:
            return __controller

    def readController(self, controller):
        try:
            self.__rBack = False
            self.__lBack = False
            __controller = controller
            self.__lValue = 0
            self.__rValue = 0
            __controller.grab()  # makes the controller only listen to this Code
            for event in __controller.read_loop():  # better with dictionary?
                if event.code == self.__LBtn:
                    self.__reverse(event, 'left')
                elif event.code == self.__LTrigger:
                    self.__lValue = event.value
                elif event.code == self.__RBtn:
                    self.__reverse(event, 'right')
                elif event.code == self.__RTrigger:
                    self.__rValue = event.value
                elif event.code == self.__StartBtn and event.value:
                    __start = time.time()
                elif event.code == self.__StartBtn and not event.value:
                    if time.time() - __start >= 5:
                        os.system('sudo shutdown now')
        except:
            print('Error while trying to read Controller output! Is the Controller connected?')

    def __reverse(self, event, side):
        __event = event
        __side = side
        if event.value:
            if __side == 'left':
                self.__lBack = True
            elif __side == 'right':
                self.__rBack = True
        elif not event.value:
            if __side == 'left':
                self.__lBack = False
            elif __side == 'right':
                self.__rBack = False

    def getValues(self):
        __lValue = 0
        __lValue = self.__lValue
        __lBack = self.__lBack
        __rValue = 0
        __rValue = self.__rValue
        __rBack = self.__rBack
        return __lValue, __lBack, __rValue, __rBack
