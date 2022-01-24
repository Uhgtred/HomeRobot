#from pynput import mouse
#from threading import Thread

#                
#def linMouse():
#    while True:
#        with mouse.Events() as events:
#            for event in events:
#                if type(event) == mouse.Events.Move:
#                    pass
#                elif event.button == mouse.Button.left:
#                    print(event.pressed)
#                    
#                    
#thread = Thread(target=linMouse)
#thread.start()

from evdev import InputDevice
import subprocess

__path = '/dev/input/'
__temp = subprocess.Popen(['ls', __path], stdout=subprocess.PIPE)
__mouse = None

__temp = __temp.communicate()
__deviceList = (__temp[0]).decode()
print(__deviceList)
print(InputDevice(f'{__path}event2').info)
__deviceList = __deviceList.split('\n')
controller = InputDevice(f'{__path}event2')
for event in controller.read_loop():
    print(event.code)
    print(event.value)
#for element in __deviceList:
#    element = f'{__path}{element}'
#    if 'event' in element:
#        if InputDevice(element).info.vendor == 12068:
#            __mouse = InputDevice(element)

