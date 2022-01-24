#!/usr/bin/env python3
# @author   Markus Kösters

import threading
from Controller.Controller import Controller
from MotorControl.PWM import PWM
from Network.SocketClient import SocketClient
from HardwareConfiguration.ConfigReader import ConfigReader
import time


class Main:

    def __init__(self):
        self.__pwmController = PWM()
        self.__conf = ConfigReader()
        self.__cont = Controller()
        self.__delay = self.__conf.readConfigParameter('DelayMain')
        self.__leftTrackForwardPin = self.__conf.readConfigParameter('LeftTrackForwardPin')
        self.__leftTrackRewardPin = self.__conf.readConfigParameter('LeftTrackRewardPin')
        self.__rightTrackForwardPin = self.__conf.readConfigParameter('RightTrackForwardPin')
        self.__rightTrackRewardPin = self.__conf.readConfigParameter('RightTrackRewardPin')
        self.__controller = None

        __controller = self.__cont.initController()
        print(__controller)

        if __controller is None:
            self.__socket = SocketClient()
            self.__socketAnswer = [0, False, 0, False]
            __socketThread = threading.Thread(target=self.__socketRead, name='SocketReadThread')
            __socketThread.daemon = True
            __socketThread.start()
        else:
            __controllerThread = threading.Thread(target=lambda: self.__cont.readController(__controller),
                                                  name='ControllerThread')
            __controllerThread.daemon = True
            __controllerThread.start()
            self.__pwmController.powerOn()          # activates the motor-board if controller is plugged in

        # setting up the pwm-motor-controller
        self.__pwmController.gpioSetup()
        self.__pwmController.channelSetup()

        # Need to start in separate processes probably Functions maybe have to be their own files for that
        __lChainThread = threading.Thread(target=self.__lChain, name='LeftChainThread')
        __lChainThread.daemon = True
        __rChainThread = threading.Thread(target=self.__rChain, name='LeftChainThread')
        __rChainThread.daemon = True
        __lChainThread.start()
        __rChainThread.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print('Program exit, resetting GPIO-Pins...')
        finally:
            self.__exit_handler()

    def __socketRead(self):
        while True:
            self.__socketAnswer = self.__socket.rcvCommands()
            if self.__socketAnswer[2] or self.__socketAnswer[0]:
                self.__MotorStatus = 'Driving'  # saving power by toggling motor-driver-channels
                self.__pwmController.powerOn()  # saving power by toggling motor-driver-channels
            else:
                self.__MotorStatus = 'Standing'  # saving power by toggling motor-driver-channels
                self.__pwmController.standBy()  # saving power by toggling motor-driver-channels
            time.sleep(self.__delay)

    def __lChain(self, controller=None):
        __pwmControllerLocal = PWM()
        __controller = controller
        if __controller:
            __contValues = []
        while True:
            if self.__controller is None:
                __pwmControllerLocal.moveTrack(self.__leftTrackForwardPin, self.__leftTrackRewardPin, self.__socketAnswer[0], self.__socketAnswer[1])
            else:
                __contValues = self.__cont.getValues()
                __pwmControllerLocal.moveTrack(self.__leftTrackForwardPin, self.__leftTrackRewardPin, __contValues[0], __contValues[1])
            time.sleep(self.__delay)

    def __rChain(self, controller=None):
        __pwmControllerLocal = PWM()
        __controller = controller
        if __controller:
            __contValues = []
        while True:
            if self.__controller is None:
                __pwmControllerLocal.moveTrack(self.__rightTrackForwardPin, self.__rightTrackRewardPin, self.__socketAnswer[2], self.__socketAnswer[3])
            else:
                __contValues = self.__cont.getValues()
                __pwmControllerLocal.moveTrack(self.__leftTrackForwardPin, self.__leftTrackRewardPin, __contValues[2], __contValues[3])
            time.sleep(self.__delay)

    def __exit_handler(self):
        try:
            self.__socket.disconnect()
        finally:
            self.__pwmController.cleanUp()


main = Main()
