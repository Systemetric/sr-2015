from sr.robot import Robot
from CommandList import *
import Orientation as orient
import math
import random

OFFSET_X = 0 # relative to cube
OFFSET_Y = 0 # relative to cube
OFFSET_ROT_Y = 1.75 # relative to camera

class Hobo(Robot):
    """
    This will contain all of the high level competition code
    If you want to add seperate versions of competition code then add more functions
    Instead of using robot.* use self.*
    The robot should start facing anti-clockwise at the edge of the meter square within the zone
    """
    
    suck    = False #Is there something on out head
    squeeze = True #Are the arms in
    lift    = 0     #What Position the arms are in
    wrists  = 0   #What position the wrists are in
    platter = 0   #What position the platter is in
    
    debug = 1
    
    returnDistance = 0
    returnAngle = 135
    currentAngle = 0

    
    def __init__(self, debug=1):
        print('Start Hobo init')
        super(Hobo, self).__init__()
        #add_robot(self)
        self.debug = debug
        currentAngle = ((self.zone * 90) -180) % 360
        print('End Hobo init')
        
    '''def init(self):
        super(Hobo, self).init()
        #add_robot(self)
        time.sleep(12)
        commandList = [CommandWrists(CommandWrists.WRISTS_n120), CommandWrists(CommandWrists.WRISTS_90),CommandWrists(CommandWrists.WRISTS_0), CommandLift(CommandLift.LIFT_HEAD), CommandSqueeze(False)]
        self.run_commands(commandList)'''
        
    def run(self):
        """
        Run competition code
        """
        status = self.startComp2()
        if status > 0:
            self.endComp3()
        self.endComp2()
        pass

    def run_commands(self, commands):
        for c in commands:
            if isinstance(c, Command):
                
                if isinstance(c, CommandTurn):
                    self.currentAngle -= c.angle
                    self.returnAngle -= c.angle
                    if self.returnAngle > 180:
                        self.returnAngle = self.returnAngle-360
                    if self.returnAngle < -180:
                        self.returnAngle = self.returnAngle+360
                    print("Return Distance: {}, Return Angle: {}".format(self.returnDistance, self.returnAngle))
                        
                if isinstance(c, CommandDrive):
                    distDriven = c.distance
                    self.returnDistance = math.sqrt((distDriven * distDriven) + (self.returnDistance * self.returnDistance) - (self.returnDistance * distDriven * 2 * math.cos(math.radians(self.returnAngle))))
                    if self.returnDistance == 0 :
                        self.returnAnlge = 0
                    else:
                        self.returnAngle = self.returnAngle + math.degrees(math.asin((distDriven / self.returnDistance) * math.sin(math.radians(self.returnAngle))))
                    print("Return Distance: {}, Return Angle: {}".format(self.returnDistance, self.returnAngle))
                    
                if isinstance(c, CommandSqueeze):
                    if c.enable == self.squeeze:
                        continue
                    else:
                        self.squeeze = c.enable
                        
                if isinstance(c, CommandLift):
                    if c.position == self.lift:
                        continue
                    else:
                        self.lift = c.position
                        
                if isinstance(c, CommandWrists):
                    if c.position == self.wrists:
                        continue
                    else:
                        self.wrists = c.position
                        
                if isinstance(c, CommandPlatter):
                    if c.position == self.platter:
                        continue
                    else:
                        self.platter = c.position
                        
                if isinstance(c, CommandSuck):
                    if c.enable == self.suck:
                        continue
                    else:
                        self.suck = c.enable
                
                c.run()
            else:
                raise TypeError("Expected {}, Recieved {}".format(type(c), type(Command)))
     
    def panicComp(self):
        ''' Drives to cube that has our face up, brings to our zone 
            Repeats looking for cubes (accidentally) turned to our face up '''
        
        # Fetch our cube
        self.run_commands([CommandDrive(2.5),
                           CommandTurn(-90),
                           CommandDrive(2.5),
                           CommandTurn(-135),
                           CommandDrive(3.5),
                           CommandPlatter(4)])
        '''#Push the central cubes to an edge - stop others collecting them.     
        self.run_commands([CommandDrive(-1),
                           CommandTurn(135),
                           CommandDrive(2.25),
                           CommandTurn(90),
                           CommandDrive(5),
                           CommandDrive(-3.5)])
                           
        # In center of arena
        while True:
            markers = self.find_cube()
            while markers is not False:
                self.move_to_cube(markers[0])
                self.go_home()
                self.run_commands([CommandDrive(-1),CommandTurn(180)])
            
                markers = self.find_cube()
            self.run_commands([CommandDrive((2*random.random())-1),CommandTurn(random.randrange(-90,90))])
            
        #while True:
        #    #Troll the other robots
        #    self.run_commands([CommandTurn(90), CommandDrive(3.5)])
        '''                       
    def go_home(self):
        self.run_commands([CommandTurn(self.returnAngle),CommandDrive(self.returnDistance)])
        
    def put_down(self, cubeList):
        for movement in cubeList:
            self.run_commands(movement)
            self.run_commands([CommandDrive(-0.3)])
        self.run_commands([CommandDrive(1),CommandDrive(-0.5),CommandTurn(180)])
    
    def comp1(self):
        commandList = [CommandTurn(-45)]
        commandList += drive_to_point(1, 7, False)
        
    def startComp2(self):
        ''' Gets edge cube then centre cube then drives back (through corner cube?)
        
        returns:
         2 : has got all cubes and returned home
         1 : has returned home
        -1 : hasn't got any cubes
        -2 : cant solve a cube, hasn't got any
        '''
        startMove1 = None
        startMove2 = None
        endMove1 = None
        endMove2 = None
        # Edge Cube
        commandList = [CommandDrive(3), CommandTurn(-90)]
        self.run_commands(commandList)
        
        marker = select_marker(self.see_cube(),self.zone, not self.suck)
        if marker == False:
            return -1    
        
        if marker.dist > 2:
            skip = True
        else:
            skip = False
        
        if not skip:
            markerReturned = self.move_to_cube(marker)
        
        
            (startMove1,endMove1) = orient.getRotation(orient.getOrient(markerReturned,self.zone),markerReturned,not self.suck)
            
            if startMove1 == None:
                return -2
                
            self.run_commands(startMove1)
        
        
            # Centre Cube
            marker= select_marker(self.see_cube(),self.zone, not self.suck)
            if marker == False:
                dist = (math.tan(math.pi/2) * math.cos(math.radians(self.returnAngle)) * self.returnDistance) - math.sin(math.radians(self.returnAngle))
                self.run_commands([CommandDrive(dist)])
                self.go_home()
                self.put_down([endMove1])
                return 1
            
        
        marker = self.move_to_cube(marker)
        if marker == False:
            
            if skip:
                return -1
                
            dist = (math.tan(math.pi/2) * math.cos(math.radians(self.returnAngle)) * self.returnDistance) - math.sin(math.radians(self.returnAngle))
            self.run_commands([CommandDrive(dist)])
            self.go_home()
            self.put_down([endMove1])
            return 1
            
        
        (startMove2,endMove2) = orient.getRotation(orient.getOrient(marker,self.zone),marker, not self.suck)
        if startMove2 == None:
            
            if skip:
                return -2

            dist = (math.tan(math.pi/2) * math.cos(math.radians(self.returnAngle)) * self.returnDistance) - math.sin(math.radians(self.returnAngle))
            self.run_commands([CommandDrive(dist)])
            self.go_home()
            self.put_down([endMove1])
            return 1            
            
        self.run_commands(startMove2)
        
        # Going Home
        commandList = [CommandDrive(.3),CommandTurn(self.returnAngle)]
        self.run_commands(commandList)
        self.go_home()
        self.put_down([[],endMove2,endMove1])
        return 2
 
    def startComp3(self):
        ''' Gets edge cube then centre cube then drives back (through corner cube?) '''
        commandList = [CommandDrive(3),CommandTurn(-90),CommandDrive(3.5)]
        self.run_commands(commandList)
        markers = self.see_cube()
        marker = select_marker(markers,self.zone,not self.suck)
        (startMove1,endMove1) = orient.getRotation(orient.getOrient(marker,self.zone),marker,not self.suck)
        if (markers != None) and (startMove1 != None):
            self.move_to_cube(marker)
            self.run_commands(startMove1 + [CommandTurn(90)])
        markers = self.see_cube()
        marker = select_marker(markers,self.zone,not self.suck)
        (startMove2,endMove2) = orient.getRotation(orient.getOrient(marker,self.zone),marker,not self.suck)
        if (markers != None) and (startMove2 != None):
            self.move_to_cube(marker)
            self.run_commands(startMove1 + [CommandDrive(-1.2),CommandTurn(self.returnAngle),CommandDrive(self.returnDistance)])
        else:
            self.run_commands([CommandTurn(90)])
            markers = self.see_cube()
            marker = select_marker(markers,self.zone,not self.suck)
            (startMove2,endMove2) = orient.getRotation(orient.getOrient(marker,self.zone),marker,not self.suck)
            if (markers != None) and (startMove2 != None):
                self.move_to_cube(marker)
                self.run_commands(startMove1 + [CommandDrive(-1.2),CommandTurn(self.returnAngle),CommandDrive(self.returnDistance)])
            else:
                self.run_commands([CommandDrive(-.3),CommandTurn(self.returnAngle),CommandDrive(self.returnDistance)])
        self.run_commands([CommandDrive(.5),CommandDrive(-.3)] + endMove2 + [CommandDrive(-.3)] + endMove1 + [CommandDrive(.5),CommandDrive(-.4),CommandTurn(90 - self.currentAngle)]) 
     
    
     
    def endComp1(self):
        ''' Drives round randomly looking for cubes '''
        while True:
            markers = self.find_cube()
            if markers != False:
                marker  = select_marker(markers,self.zone,not self.suck)
                marker  = self.move_to_cube(marker)
                (startMove,endMove) = orient.getRotation(orient.getOrient(marker,self.zone),marker,not self.suck)
                if startMove != None:
                    self.run_commands(startMove)
                    self.run_commands(endMove)
                self.run_commands([CommandDrive(-0.3),CommandTurn(90),CommandDrive(1)])
                
            angle = random.choice([0,90,180,270])
            self.run_commands([CommandTurn(angle),CommandDrive(1)])
    
    def endComp2(self, Home = True):
        ''' Drives to centre (from home) then looks for and solves cubes '''
        if Home:
            commandList = [CommandTurn(45),CommandDrive(3),CommandTurn(-90),CommandDrive(3.5)]
            self.run_commands(commandList)
        while True:
            markers = self.find_cube()
            if markers != False:
                marker = select_marker(markers,self.zone,not self.suck)
                if marker != None:
                    self.move_to_cube(marker)
                    (startMove,endMove) = orient.getRotation(orient.getOrient(marker,self.zone),marker,not self.suck)
                    self.run_commands(startMove+ [CommandDrive(1)] + endMove + [CommandDrive(-1)])
                self.run_commands([CommandTurn(15)])
            else:
                angle = random.choice([0,90,180,-90])
                self.run_commands([CommandTurn(angle),CommandDrive(1)])
                
    def endComp3(self):
        ''' Circles other peoples zones looking for cubes and returning them - breaks if no cubes in other corners'''
        self.run_commands([CommandTurn(45)])
        count = 0
        while count < 4:
            self.run_commands([CommandDrive(6)])
            markers = self.see_cube()
            if len(markers) == 0:
                self.run_commands([CommandDrive(1),CommandTurn(-90)])
                count += 1
            else:
                marker = select_marker(markers,self.zone,not self.suck)
                (start,end) = orient.getRotation(orient.getOrient(marker,self.zone),marker,not self.suck)
                self.move_to_cube(marker)
                self.run_commands(start + [CommandTurn(self.returnAngle),CommandDrive(self.returnDistance)])
                self.run_commands(end + [CommandDrive(-1), CommandTurn(180)])
                count = 0
                
    def find_cube(self, stepAngle=15, maxAngle=360, marker_function = None):
        '''
        Turns in steps of stepAngle until a cube marker is found or goes past a specified angle (maxAngle)
        To turn the other way make stepAngle and maxAngle negative
        If no cube was found then returns false
        '''
        if marker_function is None:
            marker_function = should_go_to_marker
        markers = self.see_cube()
        newMarkers = []
        for m in markers:
            if marker_function(m, self.zone, True):
                newMarkers.append(m)
        markers = newMarkers
        angleTurned = 0
        while len(markers) == 0:
            if angleTurned>maxAngle:
                return False
            elif angleTurned+stepAngle>maxAngle:
                angleTurned += maxAngle-angleTurned
                self.run_commands([CommandTurn(maxAngle-angleTurned, 1)])
            else:
                angleTurned += stepAngle
                self.run_commands([CommandTurn(stepAngle, 1)])
                
            markers = self.see_cube()
            newMarkers = []
            for m in markers:
                if marker_function(m, self.zone, True):
                    newMarkers.append(m)
            markers = newMarkers
            
        return markers
                
    def see_cube(self):
        '''
        Like Robot.see() but filters our markers that are not cube markers
        '''
        markers = self.see()
        newMarkers = []
        for m in markers:
            if m.info.marker_type != MARKER_ARENA and m.info.marker_type != MARKER_ROBOT:
                newMarkers.append(m)
        return newMarkers
                
    def move_to_cube(self, marker=None, farThreshold=1.5, nearThreshold=.7, finalDistance = .05):
        print('marker(Hobo): ' + str(marker))
        self.run_commands([CommandSqueeze(False)])
        while True:
            print("searching for markers")
            markers = self.see_cube()
            
            if markers==None:
                print "No markers found"
                return False
                
            m=None
            
            if marker==None:
                if len(markers)>0:
                    marker = select_marker(markers, not self.suck)
                else:
                    print 'cannot see any markers'
                    return False
            
            bestMarker = None
                
            for m in markers:
                if m.info.code == marker.info.code:
                    if bestMarker == None:
                        bestMarker = m
                    elif m.dist > bestMarker.dist:
                        bestMarker = m
        
            m = bestMarker
            
            if m==None:
                print "No valid markers found"
                return False
            
            length, alpha, beta = correction(m.dist, m.rot_y, m.orientation.rot_y)
            
            if(length>farThreshold):
                commandList = drive_to_cube(m, (farThreshold+2*nearThreshold)/3)
            elif(length>nearThreshold+.01):
                commandList = align_to_cube(m, nearThreshold)
            else:
                if(abs(beta)>15):
                    commandList = align_to_cube(m, (farThreshold+2*nearThreshold)/3)
                else:
                    commandList = [CommandSqueeze(False), CommandLift(CommandLift.LIFT_HEAD, 3)] + drive_to_cube(m, finalDistance)
                    self.run_commands(commandList)
                    markers = self.see_cube()
                    
                    if markers==None:
                        print "No markers found"
                        return False
                        
                    mLast=None
                    
                    print('marker: ' + str(marker))
                    if marker==None:
                        if len(markers)>0:
                            mLast=markers[0]
                        else:
                            mLast=None
                    else:
                        bestMarker = None
                            
                        for mLast in markers:
                            if mLast.info.code == marker.info.code:
                                if bestMarker == None:
                                    bestMarker = mLast
                                elif mLast.dist > bestMarker.dist:
                                    bestMarker = mLast
                    
                        mLast = bestMarker
                    if mLast==None:
                        print "Probably successful"
                        return m
                    else:
                        commandList = []
            
            self.run_commands(commandList)
                
            print("done step\n")
            print("Restarting...")
            
    def warm_up_wrists(self):
        '''
        Continuouly move wrists to prepare robot
        '''
        
        while True:
            self.run_commands([CommandWrists(2), CommandWrists(0)])
                
def drive_to_point(x, y, endFacingSameDirection=True):
    '''
    Gets a Command List to drive strait to the cartesian point (x, y) relative to the current position of the robot
    If endFacingSameDirection is true the the robot will make a turn once it has reached to point so that the direction it is facing is the same as it started
    
    '''
    theta = math.degrees(math.atan2(x, y)) #Angle to turn
    length = math.sqrt(x*x+y*y) #Distance to drive
    
    commandList = [CommandTurn(theta), CommandDrive(length)]
    if endFacingSameDirection:
        commandList.append(CommandTurn(-theta))
    
    return commandList
    
def drive_to_cube(marker, clearance=1.2):
    '''
    Gets a Command List to drive strait to a cube marker
    The clearance defines how far from the marker to stop
    '''
    alpha = marker.centre.polar.rot_y
    distance = marker.dist-clearance
    distance, alpha, beta = correction(distance, alpha, 0)
    return [CommandTurn(alpha), CommandDrive(distance)]
    
def align_to_cube(marker, clearance=1):
    '''
    Gets a Command List to align the robot so that it is directly infront of a cube and facing the cube
    The clearance is how far away the robot should be once aligned
    
    This function does not work well at distances greater than 2 metres due to unreliability in the orientation of the cube
    This function is not always acurate so may have to be run multiple times before the robot is aligned
    '''
    alpha = marker.centre.polar.rot_y #angle between camera normal and cube centre
    beta =  marker.orientation.rot_y  #angle between camera cube length and cube normal
    
    length = marker.centre.polar.length #distance between camera and cube
    
    length, alpha, beta = correction(length, alpha, beta)
    
    xSquared = length*length+clearance*clearance-2*length*clearance*math.cos(math.radians(beta))
    x = math.sqrt(xSquared) #distance to drive
    
    mu = math.copysign(math.degrees(math.asin(clearance/x*math.sin(math.radians(beta)))), -beta) #originally used to calculate both theta and gamma
    if(length<clearance):
        mu=180-mu
    theta = alpha+mu #first distance to turn
    gamma = beta-mu #distance to turn to face cube
    print("length:{:.2f}, alpha:{:.2f}, beta:{:.2f} --> x:{:.2f}, mu:{:.2f}, theta:{:.2f}, gamma:{:.2f}\n".format(length, alpha, beta, x, mu, theta, gamma))
    return [CommandTurn(theta), CommandDrive(x), CommandTurn(gamma)]
        
def drive_to_side_of_cube(marker, clearance=1):
    alpha = marker.centre.polar.rot_y #angle between camera normal and cube centre
    beta =  marker.orientation.rot_y  #angle between camera cube length and cube normal
    length = marker.centre.polar.length #distance between camera and cube
    
    offsetX = math.copysign(clearance+.1, beta)
    offsetY = .1
    absOffsetSquared = offsetX*offsetX+offsetY*offsetY
    absOffset = math.sqrt(absOffsetSquared)
    
    rho = math.degrees(math.atan2(offsetX,offsetY))
    aey = 180-abs(beta)+abs(rho)
    r = math.sqrt(length*length+absOffsetSquared-2*length*absOffset*math.cos(math.radians(aey)))
    theta = math.degrees(math.asin(absOffset/r*math.sin(math.radians(aey))))-alpha
    
    gamma = -(rho + math.copysign(90, -theta) + aey + theta + alpha)
    
    print("length:{:.2f}, alpha:{:.2f}, beta:{:.2f} offsetX:{:.2f}, offsetY:{:.2f}-->absOffset:{:.2f}, rho:{:.2f}, aey:{:.2f}, theta:{:.2f}, gamma:{:.2f}, r:{:.2f}\n".format(length, alpha, beta, offsetX, offsetY, absOffset, rho, aey, theta, gamma, r))
    
    return [CommandTurn(theta), CommandDrive(r), CommandTurn(gamma)]
        
def correction(length, alpha, beta):
    '''
    This correction ajusts the polar coordinate of a marker to ajust for camera offsets
    The parameters are:
        length: Marker.dist (Marker.centre.polar.length)
        alpha:  Marker.rot_y (Marker.centre.polar.rot_y)
        beta:   Marker.orient.rot_y
    Returns (length, alpha, beta)
    Uses the Constants
        OFFSET_X:     Ajusts cartisian x relative to cube
        OFFSET_Y:     Ajusts cartesian y relative to cube
        OFFSET_ROT_Y: Ajusts alpha relative to camera
    '''
    length0 = length
    alpha0 = math.radians(alpha+OFFSET_ROT_Y)
    beta0 = math.radians(beta)
    x0 = length0*math.cos(beta0)
    y0 = length0*math.sin(beta0)
   
    y1 = y0 + OFFSET_Y
    x1 = x0 + OFFSET_X
    
    length1 = math.sqrt(x1*x1 + y1*y1)
    beta1 = math.asin(y1/length1)
    alpha1 = alpha0 + beta0 - beta1
    
    return length1, math.degrees(alpha1), math.degrees(beta1) 
    
def should_go_to_marker(marker, target=0, usePlatter = True):
    targetOrient = orient.getOrient(marker, target)
    if targetOrient == orient.Side.top:
        return False
    if not usePlatter and (targetOrient == orient.Side.right or targetOrient == orient.Side.left):
        return False
    return True
    
def is_target_up(marker, target, _):
    targetOrient = orient.getOrient(marker, target)
    return targetOrient == orient.Side.top
    
def select_marker(markers, target=0, usePlatter = True):
    bestMarker = None
    for marker in markers:
        if should_go_to_marker(marker, target, usePlatter):
            if bestMarker==None:
                bestMarker=marker
            elif bestMarker.dist>marker.dist:
                bestMarker = marker
    return bestMarker
                
                
                
                
                
                
                
                
            
            
            
            
            
            
