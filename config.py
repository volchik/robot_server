#!/usr/bin/env python
# coding: utf-8
import os
from configobj import ConfigObj


class Config(object):
    def __init__(self, filename):
        config = ConfigObj(filename, unrepr=True)
        self.__dict__.update(config)
        config_dir = os.path.abspath(os.path.dirname(filename))

        self.www_host = config.get('www.host', '')
        self.www_port = config.get('www.port', 8080)
        www_home      = config.get('www.home', 'www')
        self.www_home = os.path.join(config_dir, www_home)
        self.www_main = config.get('www.main', 'main.html')

        log_filename      = config.get('log.filename', 'log/www.log')
        self.log_filename = os.path.join(config_dir, log_filename)

        pid_filename      = config.get('pid.filename', 'pid/www.pid')
        self.pid_filename = os.path.join(config_dir, pid_filename)

        self.robot_port     = config.get('robot.port',     '/dev/ttyUSB0')
        self.robot_baudrate = config.get('robot.baudrate', 9600)

        self.cam_num     = config.get('cam.num',  6)
        self.cam_mode    = config.get('cam.mode', 1)
        self.cam_fps     = config.get('cam.fps', -1)
        self.cam_quality = config.get('cam.quality', 70)


if __name__ == '__main__':
    filename = os.path.abspath('server.conf')
    print filename

    Config = Config(filename)
    print '"' + str(Config.www_host) + '"'
    print '"' + str(Config.www_port) + '"'
    print '"' + str(Config.pid_filename) + '"'

