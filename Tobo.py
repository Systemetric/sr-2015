from sr.robot import *
from Hobo import *
import time
import Communication as movement
#from rugged import movement
import math
import util
import MoveToCubeTest
import Orientation as orient
from CommandList import *

class Tobo(Hobo):
    """
    This is where the test functions go
    Instead of using robot.* use self.*
    """
    CAMERA_TO_ROT_CENTRE = .08
    CAMERA_ROT_ERROR = -1 # degrees off (ish)
    CAMERA_X_OFFSET  = 0
    
    OFFSET_X = 0.03 # relative to cube
    OFFSET_Y = 0.1 # relative to cube
    OFFSET_ROT_Y = 0 # relative to camera
            
    def do_everything(self):
        commandList = [CommandDrive(2), CommandDrive(-2), CommandTurn(90), CommandTurn(-90), CommandPlatter(CommandPlatter.PLATTER_90_DEGREES),CommandLift(CommandLift.LIFT_HEAD),CommandLift(CommandLift.LIFT_GROUND),CommandWrists(CommandWrists.WRISTS_0),CommandWrists(CommandWrists.WRISTS_90),CommandSqueeze(False),CommandSqueeze(True), CommandPlatter(CommandPlatter.PLATTER_0_DEGREES), CommandSuck(True), CommandSuck(False)]
        self.run_commands(commandList)
        
    def initialize(self):
        commandList = [CommandWrists(CommandWrists.WRISTS_n120), CommandWrists(CommandWrists.WRISTS_90),CommandWrists(CommandWrists.WRISTS_0), CommandLift(CommandLift.LIFT_HEAD), CommandSqueeze(False)]
        self.run_commands(commandList)
            
    def test_decision(self):
        marker = None
        while marker==None:
            markers = self.see()
            marker = select_marker(markers, 0, True)
        commandList = drive_to_cube(marker, .2)
        self.run_commands(commandList)
            
    def test_return(self):
        self.move_to_cube()
        
        commandList = [CommandTurn(self.returnAngle), CommandDrive(self.returnDistance)]
        self.run_commands(commandList)
            
    def see_test(self, ajustMarkers=False, checkReliablility=0):
        markers = None
        if checkReliablility:
            markers = self.markerReliabilityCheck(checkReliablility)
        else:
            markers = super(Tobo, self).see()
        if ajustMarkers:
            for m in markers:
                if (m.info.marker_type == MARKER_TOKEN_TOP or 
                m.info.marker_type == MARKER_TOKEN_SIDE or 
                m.info.marker_type == MARKER_TOKEN_BOTTOM):
                        alpha0 = m.centre.polar.rot_y + self.OFFSET_ROT_Y
                        beta0 =  math.radians(m.orientation.rot_y)
                        length0 = m.centre.polar.length
                        
                        y0 = length0 * math.cos(math.radians(beta0))
                        x0 = length0 * math.sin(math.radians(beta0))
                        
                        y1 = y0 + self.OFFSET_Y
                        x1 = x0 + self.OFFSET_X
                        
                        length1 = math.sqrt(x1*x1 + y1*y1)
                        
                        beta1 = math.degrees(math.asin(x1/length1))
                        alpha1 = beta1 - (alpha0 - beta0)
                        
                        m.centre.polar.rot_y = alpha1
                        m.orientation.rot_y = beta1
                        m.centre.polar.length = length1
        return markers
    
    def markerReliabilityCheck(self, markerCount, alphaWeight=1, betaWeight=5, lengthWeight=2):
        markers = {}
        for i in range(markerCount):
            ms = super(Tobo, self).see_cube()
            for m in ms:
                mCode = str(m.info.code)
                if mCode in markers:
                    markers[mCode]["marker"].append(m)
                    markers[mCode]["alpha"].append(m.centre.rot_y)
                    markers[mCode]["beta"].append(m.orientation.rot_y)
                    markers[mCode]["length"].append(m.centre.dist)
                    
                else:
                    markers.update({mCode:{"marker": [m], "alpha":[m.centre.rot_y], "beta": [m.orientation.rot_y], "length": [m.centre.dist]}})
        for key in list(markers):
            mDict = markers[key]
            
            sqrtN = math.sqrt(len(mDict["marker"]))
            
            alphaXBar = util.mean(mDict["alpha"])
            alphaSd = util.stdev(mDict["alpha"])/sqrtN
            betaXBar = util.mean(mDict["beta"])
            betaSd = util.stdev(mDict["beta"])/sqrtN
            lengthXBar = util.mean(mDict["length"])
            lengthSd = util.stdev(mDict["length"])/sqrtN
            
            error = (alphaWeight*alphaSd + betaWeight*betaSd + lengthWeight*lengthSd) / (alphaWeight + betaWeight + lengthWeight)
            for m in mDict["marker"]:
                m.error = error
            
            
    
    def __init__(self):
        super(Tobo, self).__init__()
        
    def list_markers(self):
        markers = self.see()
        print ("I can see {0} markers".format(len(markers)))
        for marker in markers:
            if marker.info.marker_type == MARKER_TOKEN_SIDE:
                print('The orientation of marker {0} is: {1}'.format(repr(marker), str(marker.orientation)))
                    
    def test_link(self):
        movement.drive(1)
        time.sleep(5)
        movement.turn(90)
        time.sleep(5)
        movement.drive(-1)
        time.sleep(5)
        movement.turn(-90)
        time.sleep(5)
        movement.movePlatter(0)
        time.sleep(5)
        movement.movePlatter(1)
        time.sleep(5)
        movement.movePlatter(2)
        time.sleep(5)
        movement.movePlatter(3)
        time.sleep(5)
        movement.movePlatter(4)
        time.sleep(5)
            
    def move_square(self, sleeptime=2):
        """
        Move in a square
        """
        for i in range(4):
            movement.drive(1)
            time.sleep(sleeptime)
            movement.turn(90)
            time.sleep(sleeptime)
            
    def move_m(self, distance=1):
        movement.drive(distance)
            
    def move_snake(self, sleeptime=2):
        """
        Move in a square
        """
        for turn in [90,-90]:
            for i in range(2):
                movement.drive(.5)
                time.sleep(sleeptime)
                movement.turn(turn)
                time.sleep(sleeptime)
        
            
    def move_to_cube_old(self, marker):
        """
        Try to move to a marker
        """
        rot=marker.rot_y
        dist=marker.dist
        rot, dist2 = self.adjust_angle(rot,dist)
        direction_turned = math.copysign(90, rot)
        print("Turning 90 degrees {0}clockwise.".format("anti"*(direction_turned==-90)))
        movement.turn(direction_turned)
        print("Driving...")
        movement.drive(dist*abs(math.sin(math.radians(rot))))
        print("Turning 90 degrees {0}clockwise.".format("anti"*(direction_turned==90)))
        movement.turn(-direction_turned)
        print("Driving...")
        movement.drive(dist*math.cos(math.radians(rot)))
        
    def move_to_cube_improved(self):
        MoveToCubeTest.moveToCubeImproved(self)
        
    def camera_error_calibration(self):
        '''
        Do not run during other logic is a locking function - this does not account for error, but allows humans to fix camera
        For use:
        Put a box directly ahead of the robot, with it facing the camera.
        Run this function with a device linked to the robot to get the debug output
        Ajust the camera till the outputed error is ~0 
        '''
        movement.drive(-2)
        while 1:
            markers = self.see_cube()
            rot = 0
            if(len(markers) > 0):
                rot = markers[0].rot_y
                distance = markers[0].dist
                print("Box at heading {0}, distance {1}".format(rot,distance))
                time.sleep(2)
            else:
                print("No markers seen")

    def calibrate_marker(self):
        from calibrate import CalibrateMarker
        CalibrateMarker(self)
        
    def marker_orientation(self, marker, target=''):
        from Orientation import getOrient
        if target == '':
            target = self.zone
        return getOrient(marker, target)
        
    def adjust_angle(self, angle, dist):
        opposite = math.sin(math.radians(angle))*dist
        adjacent = math.cos(math.radians(angle))*dist
        adjacent += Tobo.CAMERA_TO_ROT_CENTRE
        angle = math.atan(opposite/adjacent)
        dist = adjacent/math.cos(angle)
        return math.degrees(angle), dist
        
    def turn_ten(self):
        for i in range (0,40):
            movement.turn(90)
            time.sleep(1)
            
    def turn_back(self):
        for i in range(3):
            movement.turn(360)
            time.sleep(1)
        for i in range(3):
            movement.turn(-360)
            time.sleep(1)
            
    def alignment_test(self):
        for i in range (0,20):
            movement.drive(-.10)
            time.sleep(0.5)
            for j in range (0,5):  
                m = self.see()
                if len(m) > 0:
                    print "Distance %s \n Angle %s" %(m[0].dist,m[0].rot_y)
                else:
                    print 'cannot see marker'
                
    def arms_test(self):
        time.sleep(1)
        print ('turn to 30')
        self.run_commands([CommandWrists(CommandWrists.WRISTS_90)])
        
    def lift_test(self):
        time.sleep(10)
        print("Head")
        movement.liftArms(movement.LIFT_HEAD)
        time.sleep(10)
        print("Holding")
        movement.liftArms(movement.LIFT_HOLDING)
        time.sleep(10)
        print("Down")
        movement.liftArms(movement.LIFT_GROUND)
        time.sleep(10)
        
    def new_alignment_test(self):
        testNo = 0
        while True:
            markers = self.see()
            j=0
            while len(markers)<1:
                markers = self.see()
                if j%100==0: print("Test {} Failed: Cannot see any markers".format(testNo))
                j+=1
                time.sleep(0.1)
            dist = []
            angle = []
            for i in range(50):
                markers = self.see()
                j=0
                if len(markers)>0:
                    dist.append(markers[0].dist)
                    angle.append(markers[0].rot_y)
                else:
                    print("Test {} Failed: Lost marker".format(testNo))
                    break
            if len(dist)==50 and len(angle)==50:
                print("Dist{}{}".format(testNo, dist))
                print("Angle{}{}".format(testNo, angle))
                testNo+=1
                
    def solving_test(self):
        while True:
            print "starting"
            markers = self.see_cube()
            print "searching for markers"
            while len(markers)<=0:
                markers = self.see_cube()
            
            print "found marker"
            m = markers[0]
            
            ori = orient.getOrient(m)
            
            commands1, commands2 = orient.getRotation(ori, m, False, 1)
            
            if commands1==None or commands2==None:
                print "invalid position"
                continue
            print "running setup commands"
            self.run_commands(commands1)
            print "running putdown commands"
            self.run_commands(commands2)
            print "DONE, RESTARTING"
            
    def full_drive_to_cube(self):
        marker = None
        while marker == False or marker==None:
            marker= select_marker(self.see_cube(),self.zone, not self.suck)
        print('marker: ' + str(marker))
        marker = self.move_to_cube(marker)
        
        if marker != False:
            (startMove,endMove) = orient.getRotation(orient.getOrient(marker,self.zone),marker,not self.suck)
            if startMove != None:
                self.run_commands(startMove)
                commands = [CommandTurn(self.returnAngle - self.currentAngle),CommandDrive(self.returnDistance)]
                self.run_commands(commands)
                self.run_commands(endMove)
            
        
    
        
        
        
        
    
