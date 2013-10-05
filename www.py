#!/usr/bin/python
# coding: utf-8

import sys, time
from daemon import Daemon

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import threading
import cgi
import string, sys, time
import os
from cv2 import cv
import Image, ImageDraw, ImageFont
#import StringIO
#my import
from const  import *
from robot  import Robot
from config import Config

#cam property
#see server.conf
ResMode = ((352, 288), (640, 480), (1280,1024))
textColor = cv.RGB(255,255,255)


#Web Port
#see server.conf
refreshTime = 5 #every xx sec

#DIRS
#see server.conf


class MyHandler(BaseHTTPRequestHandler):	
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_AUTHHEAD(self):
        if self.path == "/":
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm=\"Robot control\"')
        else:
            self.send_response(200)
		
    def do_Auth(self):
        if self.headers.get('Authorization') == 'Basic YWRtaW46cXdlcnR5':
            return True
        else:
            self.do_AUTHHEAD()
            self.log_error("[AUTH] Not authenticated")
            return False

    def showAuthResult(self,message):
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write("<html>")
        self.wfile.write("<head>")
        self.wfile.write("<title>Login page</title>")
        self.wfile.write("</head>")
        self.wfile.write("<body>")
        self.wfile.write("<p>")
        self.wfile.write(message)
        self.wfile.write("</p>")
        self.wfile.write("</body>")
        self.wfile.write("</html>")

    def showPage(self,method,get_data,post_data):
        if get_data.get('action') != None:
            action = get_data.get('action')[0]
        else: action = ""

        if action == "mjpeg": #get mjpeg
            self.send_response(200)
            self.wfile.write("Content-Type: multipart/x-mixed-replace; boundary=--aaboundary")
            self.wfile.write("\r\n\r\n")
            if not self.server.capture:
                return
            t = time.time()
            frameCount = 0
            frameFps = 0
            frameSize = 0
            frameSpeed = 0
            self.log_error("[WEBCAM] start while")
            #while server runed
            while self.server.run:
                #try:
                    frameCount = frameCount + 1
                    img = cv.QueryFrame(self.server.capture)

                    text = time.strftime("%d/%m/%Y %H:%M:%S",time.localtime())
                    textSize, baseline = cv.GetTextSize(text,self.server.font)
                    cv.PutText(img,text, (textSize[1],2*textSize[1]),self.server.font, textColor)
                    text = str(frameSpeed)+"kb/s"
                    text = text +"  "+str(frameFps)+"fps"
                    textSize, baseline = cv.GetTextSize(text,self.server.font)
                    cv.PutText(img,text, (self.server.camWidth-textSize[0]-textSize[1],self.server.camHeight-textSize[1]), self.server.font, textColor)

                    cv2mat=cv.EncodeImage(".jpeg",img,(cv.CV_IMWRITE_JPEG_QUALITY,self.server.camQlt))
                    JpegData=cv2mat.tostring()
                    self.wfile.write("--aaboundary\r\n")
                    self.wfile.write("Content-Type: image/jpeg\r\n")
                    self.wfile.write("Content-length: "+str(len(JpegData))+"\r\n\r\n" )
                    self.wfile.write(JpegData)
                    self.wfile.write("\r\n\r\n\r\n")
                    if time.time() - t > refreshTime : #every Step sec
                        t = time.time()
                        frameFps = round(frameCount/refreshTime,1)
                        frameCount = 0
                        frameSize = len(JpegData)/1024
                        frameSpeed = int(8*len(JpegData)*frameFps/1024)
                        text = "Capture %s fps" % str(frameFps)
                        text = text + ", Frame size: "+str(frameSize)+"kB"
                        text = text + ", Capture speed: "+str(frameSpeed)+"kb/s"
                        self.log_error("[WEBCAM] " + text)
                        #if not self.do_Auth():
                            #self.log_error("Not authenticated")
                            #break
                    #time.sleep(0.05)
                    cv.WaitKey(20)
                #except:
                    #time.sleep(1)
                    #break 
            self.log_error("[WEBCAM] stop while")
        elif action == "jpeg": #get one jpeg
            self.send_response(200)
            self.send_header('Content-type','image/jpeg')
            self.end_headers()
            img = cv.QueryFrame(self.server.capture)
            cv2mat=cv.EncodeImage(".jpeg",img,(cv.CV_IMWRITE_JPEG_QUALITY,self.server.camQlt))
            JpegData=cv2mat.tostring()
            self.wfile.write(JpegData)
        elif action == "temperature": #get temperature
            text =  self.server.robot.getTemperature()
            self.wfile.write(text)
        elif action == "pressure": #get pressure"
            temp = int(self.server.robot.getPressure())
            text = str(int(temp/133.33))
            #text = self.server.robot.getPressure()
            self.wfile.write(text)
        elif self.path != "/": #get content
            #check allow ext
            if file_allow(self.path):
                try:
                    f = open(self.server.Config.www_home + self.path)
                    self.send_response(200)
                    self.send_header('Content-type',file_type(self.path))
	            self.end_headers()
	            self.wfile.write(f.read())
                    f.close()
                    #self.log_error("file: "+self.path+" has file type "+file_type(self.path))
                except IOError:
                    self.send_error(404,'File not found: %s' % self.path)
            else: #access denied
                self.send_error(404,'File not found: %s' % self.path)
        else: #MainHTML
            try:
               f = open(self.server.Config.www_home + '/' + self.server.Config.www_main)
               self.send_response(200)
               self.send_header('Content-type',"text/html")
               self.end_headers()
               self.wfile.write(f.read())
               f.close()
            except IOError:
               self.send_error(404, "File not found: %s" % self.path)

    def do_GET(self):
        if not self.do_Auth():
            self.showAuthResult("Not authenticated")
            return

        #GET
        get_data = cgi.parse_qs(self.path[2:])
        #ShowPage
        self.showPage('GET',get_data,{})

    def do_POST(self):
        if not self.do_Auth():
            self.showAuthResult("Not authenticated")
            return

        #GET
        get_data = cgi.parse_qs(self.path[2:])
        cl, cl2 = cgi.parse_header(self.headers.get('content-length'))
        qs = self.rfile.read(int(cl))
        post_data = cgi.parse_qs(qs.decode())
        #Resolution
        if post_data.get('resolution') != None:
            if (len(post_data.get('resolution')) > 0):
                mode = post_data.get('resolution')[0]
                if ((mode >= "0") and (mode <= "2")):
                    self.server.SetResolution(int(mode))
                else: 
                    None
            return 
        #Command
        if post_data.get('action') != None:
            cmd = post_data.get('action')[0]
            result = self.server.robot.sendCommand(cmd)
            self.wfile.write(result)
            self.log_error("[COMMAND] %s" % result)
            return
        #ShowPage
	self.showPage('GET',get_data,post_data)


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    #Handle requests in a separate thread.
    def __init__(self,handler, Config):
        self.Config = Config
        HTTPServer.__init__(self,(Config.www_host,Config.www_port),handler)
        self.run = False
        self.timeout = 1 #XXX sec timeout
        self.socket.settimeout(1)
        self.capture = None
        self.font = None
        self.camNum  = self.Config.cam_num
        self.camMode = self.Config.cam_mode
        self.camFps  = self.Config.cam_fps
        self.camQlt  = self.Config.cam_quality
        #Robot
        self.robot = Robot(Config.robot_device, Config.robot_speed)

    def CamStart(self):
        self.capture = cv.CaptureFromCAM(self.camNum)
        #check cam
        try:
            cv.QueryFrame(self.capture)
        except:
            self.capture = None

        #print cv.GetCaptureProperty(self.capture, cv.CV_CAP_PROP_FPS)
        #print cv.GetCaptureProperty(self.capture,cv.CV_CAP_PROP_FRAME_WIDTH)
        #print cv.GetCaptureProperty(self.capture,cv.CV_CAP_PROP_FRAME_HEIGHT)

        if not self.capture:
            sys.stderr.write("[WEBCAM] Error opening\r")
            return

        sys.stderr.write("[WEBCAM] start capture\r")
        cv.SetCaptureProperty(self.capture,cv.CV_CAP_PROP_FPS,self.camFps)
        self.SetResolution(self.camMode)
		
    def CamStop(self):
        if not self.capture:
            del self.capture
        sys.stderr.write("[WEBCAM] stop capture\r")

    def SetResolution(self, mode):
        self.camWidth, self.camHeight = ResMode[mode]
        cv.SetCaptureProperty(self.capture,cv.CV_CAP_PROP_FRAME_WIDTH,self.camWidth)
        cv.SetCaptureProperty(self.capture,cv.CV_CAP_PROP_FRAME_HEIGHT,self.camHeight)
        self.font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 0.5*(mode+1), 0.5*(mode+1), 0, mode+1, 8)

 
    def Start(self):
        self.CamStart()
        self.run = True
        #self.serve_forever()

    def Stop(self):
        self.run = False
        self.shutdown()
        time.sleep(1)
        self.socket.close()
        self.CamStop()	
        self.robot.close()


class MyDaemon(Daemon):
    def __init__(self,Config):
        self.Config = Config
        pidfile = Config.pid_filename
        stdin   = '/dev/null'
        stdout  = '/dev/null'
        stderr  = '/dev/null'
        if Config.log_filename != "":
            stderr = Config.log_filename  
	Daemon.__init__(self, pidfile, stdin, stdout, stderr)

    def run(self):
        server = ThreadedHTTPServer(MyHandler, self.Config)
        server.Start()
        while True:
            server.handle_request()
            #time.sleep(1)
        server.Stop()

    def stop(self):
        Daemon.stop(self)


if __name__ == "__main__":

    BaseDir  = os.path.dirname(sys.argv[0])
    config_filename = "server.conf"
    config_filename = os.path.join(BaseDir, config_filename)
    Config = Config(config_filename)
    
    try:
        os.makedirs(os.path.dirname(Config.log_filename))
        os.makedirs(os.path.dirname(Config.pid_filename))
    except:
        None

    daemon = MyDaemon(Config)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
