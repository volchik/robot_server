#!/usr/bin/env python
# coding: utf-8

import serial
import time

#======================================
# Robot class 
#======================================

class Robot:
    # Constructor
    def __init__(self, port, baudrate, timeout =0.1):
        self.port     = port
        self.baudrate = baudrate
        self.timeout  = timeout
        self.connect()
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
             "light-on"    : "LO",
             "light-off"   : "LF"
             		}
    def connect(self):
        self.port = serial.Serial(self.port, self.baudrate, timeout = self.timeout)
        time.sleep(2) # waiting the initialization...
        self.busy = False

    def close(self):
        self.port.close()

    def reconnect(self):
        self.close()
        self.connect()

    def sendCommand(self, command):
        if self.commands.get(command) != None:
            result = self.invoke(self.commands.get(command))
            if result == self.commands.get(command):
                return command
            else:
                return result 
        else: return u'Неизвестная комманда "%s"' % command
                                      
    def invoke(self, command, check=True):
        #wait while busy
        while (self.busy):
            None
        #set busy
        self.busy = True
        self.port.write(command+'\r')
        result = self.port.readline().replace('\n', '').replace('\r', '')
        self.busy = False
        if check and result[0:len(command)] != command:
            return u'Error: Отправлено: "%s" Получено: "%s"' % (command, result)
        else:
            return result

    def move_forward(self):
        return self.invoke('MU')

    def move_backward(self):
        return self.invoke('MD')

    def move_left(self):
        return self.invoke('ML')

    def move_right(self):
        return self.invoke('MR')

    def cam_up(self):
        return self.invoke('CU')

    def cam_down(self):
        return self.invoke('CD')

    def cam_left(self):
        return self.invoke('CL')

    def cam_right(self):
        return self.invoke('CR')

    def get_temperature(self):
        # todo написать проверку возвращаемых значений
        return self.invoke('TG', False)[2:]

    def get_pressure(self):
        # todo написать проверку возвращаемых значений
        return self.invoke('PG', False)[2:]

    def light_on(self):
        return self.invoke('LO')

    def light_off(self):
        return self.invoke('LF')


if __name__ == '__main__':
    client = Robot('/dev/ttyUSB0', 9600)
    print client.move_forward()
    time.sleep(5)
    print client.move_backward()
    time.sleep(5)
    print client.invoke('hello, robot!')
    print client.sendCommand('W')
    time.sleep(5)
    client.close()
