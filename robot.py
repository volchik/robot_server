import serial
import time

#======================================
# Robot class 
#======================================

class Robot:
    # Constructor
    def __init__(self, device, speed):
        self.device = device
        self.port = serial.Serial(self.device, speed, timeout=0.1)
        time.sleep(1) # waiting the initialization...
        self.busy = False

        #robot command dictionary
        self.commands = {
             "mot-fwd"     : "MU",
             "mot-rev"     : "MD",
             "mot-left"    : "ML",
             "mot-right"   : "MR",
             "cam-up"      : "CU",
             "cam-down"    : "CD",
             "cam-left"    : "CL",
             "cam-right"   : "CR",
             "W"           : "CU",
             "Z"           : "CD",
             "A"           : "CL",
             "S"           : "CR",
             "light-on"    : "LO",
             "light-off"   : "LF"
             		}

    def close(self):
        self.port.close()

    def usart_writeStr(self, s):
        #wait while busy
        while (self.busy):
            None
        #set busy
        self.busy = True
        self.port.write(s+'\r')
        result = self.port.readline().replace('\n', '').replace('\r', '')
        self.busy = False
        return result

    def sendCommand(self, cmd):
        if self.commands.get(cmd) != None:
            result = self.usart_writeStr(self.commands.get(cmd))
            if result == self.commands.get(cmd):
                return cmd
            else: return "Error"
            #return result
        else: return "Unknown command"
                                      
    def getTemperature(self):
        temperature = self.usart_writeStr('TG')
        return temperature[2:] #1-2 chars command

    def getPressure(self):
        pressure = self.usart_writeStr('PG')
        return pressure[2:] #1-2 chars command

