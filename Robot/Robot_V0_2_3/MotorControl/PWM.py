#!/usr/bin/env python3
# @author   Markus Kösters

from RPi import GPIO
from HardwareConfiguration.ConfigReader import ConfigReader


class PWM:

    def __init__(self):
        self.__conf = ConfigReader()
        self.__maxFrequency = self.__conf.readConfigParameter('MaxPWMFrequency')
        self.__step = self.__conf.readConfigParameter('PWMStep')
        self.__MotorControllerPower = self.__conf.readConfigParameter('MotorBoardActivationPin')
        self.__StatusLED = self.__conf.readConfigParameter('StatusLEDPin')
        self.__channelLF = self.__conf.readConfigParameter('LeftTrackForwardPin')
        self.__channelLR = self.__conf.readConfigParameter('LeftTrackRewardPin')
        self.__channelRF = self.__conf.readConfigParameter('RightTrackForwardPin')
        self.__channelRR = self.__conf.readConfigParameter('RightTrackRewardPin')
        self.__gpioNumbering = self.__conf.readConfigParameter('GPIOPinNumbering')

    def channelSetup(self):
        """Has to be called after gpioSetup and before lChain and rChain"""
        try:
            self.powerOn()

            self.__channelLF = GPIO.PWM(self.__channelLF, self.__maxFrequency)  # gpio,frequency
            self.__channelLR = GPIO.PWM(self.__channelLR, self.__maxFrequency)  # gpio,frequency
            self.__channelLF.start(0)
            self.__channelLR.start(0)

            # Setting up 2 PWM pins for left Track
            self.__channelRF = GPIO.PWM(self.__channelRF, self.__maxFrequency)  # gpio,frequency
            self.__channelRR = GPIO.PWM(self.__channelRR, self.__maxFrequency)  # gpio,frequency
            self.__channelRF.start(0)
            self.__channelRR.start(0)
        except:
            print('Channelsetup failed! Has gpioSetup been called before?')

    def gpioSetup(self):
        """Has to be called before channelSetup"""
        try:
            GPIO.setmode(GPIO.BOARD)  # set to physical numbering of the board, gpio-numbering is GPIO.BCM
            GPIO.setwarnings(False)  # disable warnings to not spam the console

            # Setting up Pin for activation of Motor-boards and Status-LED
            GPIO.setup(self.__StatusLED, GPIO.OUT)
            GPIO.setup(self.__MotorControllerPower, GPIO.OUT)

            # Setting up 2 PWM pins for left Track
            GPIO.setup(self.__channelLF, GPIO.OUT)
            GPIO.setup(self.__channelLR, GPIO.OUT)

            # Setting up 2 PWM pins for right Track
            GPIO.setup(self.__channelRF, GPIO.OUT)
            GPIO.setup(self.__channelRR, GPIO.OUT)
        except:
            print('GPIO-Pins could not be set. Probably has been done already!')

    # def lChain(self, value, reverse):
    #     __value = int(value) * self.__step  # calculating percentage od duty cycle from controller input
    #     __value = round(__value, 1)  # rounding to 1 value after comma since GPIO does not accept more precise values
    #     __reverse = reverse
    #     if __reverse:
    #         self.__channelLF.ChangeDutyCycle(0)  # making sure moveTrack stands before reward-action
    #         self.__channelLR.ChangeDutyCycle(__value)
    #     else:
    #         self.__channelLR.ChangeDutyCycle(0)  # making sure moveTrack stands before forward-action
    #         self.__channelLF.ChangeDutyCycle(__value)
            
    #could be a more modular function:
    def moveTrack(self, pinF, pinR, value, reverse=False):
        __value = int(value) * self.__step  # calculating percentage for duty cycle from controller input
        __value = round(__value, 1)  # rounding to 1 value after comma since GPIO does not accept more precise values
        __reverse = reverse
        __pinF = pinF
        __pinR = pinR
        if __reverse:
            __pinF.ChangeDutyCycle(0)  # making sure moveTrack stands before reward-action
            __pinR.ChangeDutyCycle(__value)
        else:
            __pinR.ChangeDutyCycle(0)  # making sure moveTrack stands before forward-action
            __pinF.ChangeDutyCycle(__value)
            
    # def rChain(self, value, reverse):
    #     __value = int(value) * self.__step  # calculating percentage for duty cycle from controller input
    #     __value = round(__value, 1)  # rounding to 1 value after comma since GPIO does not accept more precise values
    #     __reverse = reverse
    #     if __reverse:
    #         self.__channelRF.ChangeDutyCycle(0)  # making sure moveTrack stands before reward-action
    #         self.__channelRR.ChangeDutyCycle(__value)
    #     else:
    #         self.__channelRR.ChangeDutyCycle(0)  # making sure moveTrack stands before forward-action
    #         self.__channelRF.ChangeDutyCycle(__value)

    def standBy(self):
        GPIO.output(self.__StatusLED, GPIO.LOW)
        GPIO.output(self.__MotorControllerPower, GPIO.LOW)

    def powerOn(self):
        GPIO.output(self.__StatusLED, GPIO.HIGH)
        GPIO.output(self.__MotorControllerPower, GPIO.HIGH)

    def cleanUp(self):
        # stopping pwm and cleaning GPIO-access
        GPIO.output(11, GPIO.LOW)
        self.__channelRR.stop()
        self.__channelLR.stop()
        self.__channelRF.stop()
        self.__channelLF.stop()
        GPIO.cleanup()
