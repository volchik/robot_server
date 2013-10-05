from I2C import I2C
import serial
import time

#======================================
# Robot class 
#======================================

class robot :
    i2c = None

    # Constructor
    def __init__(self, mode, address):
        self.mode = mode
        if self.mode == 0: #i2c mode
            self.i2c = I2C(address)
            self.address = address
        if self.mode == 1: #usart mode
            self.port = serial.Serial('/dev/ttyUSB0', 9600, timeout=0.1)
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
        if self.mode == 1:
            self.port.close()

    def cutString(self, s):
        result = s.replace('\n', '').replace('\r', '')
        return result

    def i2c_writeStr(self, s):
        #wait while busy
        while (self.busy):
            None
        #set busy
        self.busy = True
        for i in range(len(s)):
            self.i2c.write_byte(ord(s[i]))     #char to byte
        self.i2c.write_byte(13)                #end command
        self.busy = False
        return s
   
    def usart_writeStr(self, s):
        #wait while busy
        while (self.busy):
            None
        #set busy
        self.busy = True
        self.port.write(s+'\r')
        result = self.cutString(self.port.readline())
        self.busy = False
        return result

    def sendCommand(self, cmd):
        if self.commands.get(cmd) != None:
            if self.mode == 0:
	        result = self.i2c_writeStr(self.commands.get(cmd))
                if result == self.commands.get(cmd):
                    return cmd
                else: return "Error"  
#                return result
            if self.mode == 1:
                result = self.usart_writeStr(self.commands.get(cmd))
                if result == self.commands.get(cmd):
                    return cmd
                else: return "Error"
#                return result
        else: return "Unknown command"
                                      
    def getTemperature(self):
        if self.mode == 1:
            temperature = self.usart_writeStr('TG')
            return temperature[2:] #1-2 chars command

    def getPressure(self):
        if self.mode == 1:
            pressure = self.usart_writeStr('PG')
            return pressure[2:] #1-2 chars command

