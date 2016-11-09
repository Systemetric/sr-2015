import time
import serial
from definitions import *




class Arduino():
    armPos = LIFT_0
    wristPos = WRISTS_0
    platterPos = PLATTER_0
    
    def addRobot(self, robot):
        self.arduino = robot.ruggeduinos["7523031383335161C111"]
        #self.ser = serial.Serial(self.arduino, 9600)
        
    def setDirection(self, left, right):
        if not left:
            self.arduino.digital_write(3, True)
        else:
            self.arduino.digital_write(3, False)
        if right:
            self.arduino.digital_write(4, True)
        else:
            self.arduino.digital_write(4, False)
    
    def drive(self, distance):
        steps = int(abs(distance) * 8000)
        direction = False
        if distance>0:
            direction = True
        else:
            direction = False
        
        self.setDirection(direction, direction)
        
        for i in range(steps):
            self.arduino.digital_write(2, True)
            time.sleep(0.0003)
            self.arduino.digital_write(2, False)
            time.sleep(0.0003)
            
    def turn(self,angle):
        steps = int(abs(angle) * oneDegree)
        direction = False
        if angle>0:
            direction = True
        else:
            direction = False
        
        self.setDirection(direction, not direction)
        
        for i in range(steps):
            self.arduino.digital_write(2, True)
            time.sleep(0.0003)
            self.arduino.digital_write(2, False)
            time.sleep(0.0003)
            
            
    def squeezeArms(self,enable):
        if enable:
            self.arduino.digital_write(5,True)
        else:
            self.arduino.digital_write(5,False)
        
    def liftArms(self,position):
        if position == 0:
            self.armPos = LIFT_0
        if position == 1:
            self.armPos = LIFT_42
        if position == 2:
            self.armPos = LIFT_120
            
        full = self.armPos&self.wristPos&self.platterPos
        self.send(full)
            
    def moveWrists(self,position):
        if position == 0:
            self.wristPos = WRISTS_0
        if position == 1:
            self.wristPos = WRISTS_n90
        if position == 2:
            self.wristPos = WRISTS_90
        if position == 3:
            self.wristPos = WRISTS_60
        if position == 4:
            self.wristPos = WRISTS_n120
        if position == 5:
            self.wristPos = WRISTS_n30
        if position == 6:
            self.wristPos = WRISTS_unknown1
        if position == 7:
            self.wristPos = WRISTS_unknown2
                        
        full = self.armPos&self.wristPos&self.platterPos
        self.send(full)
        
    def movePlatter(self,position):
        if position == 0:
            self.platterPos = PLATTER_0
        if position == 1:
            self.platterPos = PLATTER_90
        if position == 2:
            self.platterPos = PLATTER_180
        if position == 3:
            self.platterPos = PLATTER_270
        if position == 4:
            self.platterPos = PLATTER_CR
            
        full = self.armPos&self.wristPos&self.platterPos
        self.send(full)

    def suck(self,enable):
        if enable:
            self.arduino.digital_write(6,True)
        else:
            self.arduino.digital_write(6,False)
            
    def send(self,byte):
        '''
        self.ser.write(byte)
        self.ser.flush()
        '''
        pass
        
movement = Arduino()