from CommandList import *
import Orientation as orient

"""Move to robot here"""
import time
import math
import Communication as movement
import Orientation

LENGTH_AJUSTMENT = -.1 #distance from front of robot to camera
HEIGHT_AJUSTMENT = 0 #distancce from camera to height of cube

OFFSET_X = 0 # relative to camera
OFFSET_Y = 0 # relative to camera
OFFSET_ROT_Y = 1.75 # relative to camera

finalList = []

"""class Command():
    
    COMMAND_DRIVE = 1
    COMMAND_TURN = 2
    
    def __init__(self, command, arg, delay=.5):
        self.command = command
        self.arg = arg
        self.delay = delay"""
        
def shouldGoToMarker(marker, target=0, avoidPlatter = False):
    targetOrient = orient.getOrient(marker, target)
    if targetOrient == orient.Side.top:
        return False
    if avoidPlatter and (targetOrient == orient.Side.right or targetOrient == orient.Side.left):
        return False
    return True
    
def selectMarker(markers, target=0, avoidPlatter = False):
    bestMarker = None
    for marker in markers:
        if shouldGoToMarker(marker, target, avoidPlatter):
            if bestMarker==None:
                bestMarker=marker
            elif bestMarker.length>marker.length:
                bestMarker = marker
    return bestMarker
    
def solve(marker, target=0):
    targetOrient = orient.getOrient(marker, target)
    startList, endList = orient.getRotation(orient, marker, False, 1)
    if startList==None or endList==None:
        return False
    global finalList
    finalList += endList
    return startList    
        
def moveToCubeImproved(R, farThreshold=1.5, nearThreshold=.7):
    R.run_commands([CommandSqueeze(False)])
    while True:
        print("searching for markers")
        markers = R.see()
        while len(markers)<1:
            markers = R.see()
        m = markers[0]
        
        length, alpha, beta = correction2(m.dist, m.rot_y, m.orientation.rot_y)
        
        if(length>farThreshold):
            commandList = drive_to_cube(m, (farThreshold+2*nearThreshold)/3)
        elif(length>nearThreshold+.01):
            commandList = align_to_cube(m, nearThreshold)
        else:
            if(abs(beta)>15):
                commandList = align_to_cube(m, (farThreshold+2*nearThreshold)/3)
            else:
                commandList = [CommandLift(CommandLift.LIFT_HEAD, 3), CommandSqueeze(False)] + drive_to_cube(m, .1) + [CommandLift(CommandLift.LIFT_GROUND)]
        
        R.run_commands(commandList)
            
        print("done step\n")
        
        markers = R.see()
        if(len(markers)<1):
            print("probably done\n\n")
        print("Restarting...")
        
def moveToSideOfCube(R):
    markers = R.see()
    while len(markers)<1:
        markers = R.see()
    m = markers[0]
    
    commandList = drive_to_side_of_cube(m)
        
    R.run_commands(commandList)
        
"""def readCommands(R, commandList):
    for c in commandList:
        if c.isinstance(Command):
            if c.command==Command.COMMAND_DRIVE:
                print("Driving {} meters".format(c.arg))
                movement.drive(c.arg)
            elif c.command==Command.COMMAND_TURN:
                print("Turning {} degrees".format(c.arg))
                movement.turn(c.arg)
            else:
                print("Unrecognised Command")
            print("Waiting {} seconds".format(c.delay))
            time.sleep(c.delay)
        else:
            raise TypeError("Expected {}, Recieved {}".format(type(c), type(Command)))"""
        
    
    
def getAlinementPosition(m):
    print("-----------------------------------------------")
    print("Marker code {}".format(m.info.code))
    print("Orient rotx: {:.2f},\troty: {:.2f},\trotz: {:.2f}".format(m.orientation.rot_x, m.orientation.rot_y, m.orientation.rot_z))
    print("Polar  rotx: {:.2f},\troty: {:.2f},\tlength: {:.2f}".format(m.centre.polar.rot_x, m.centre.polar.rot_y, m.centre.polar.length))
    
    alpha = m.centre.polar.rot_y #angle between camera normal and cube centre
    beta =  m.orientation.rot_y  #angle between camera cube length and cube normal
    
    length = m.centre.polar.length #distance between camera and cube
    
    """xSquared = length**2+1-2*length*math.cos(math.radians(beta))
    x = math.sqrt(xSquared)
    
    theta = math.copysign(math.degrees(math.asin(math.sin(math.radians(beta))/x)), beta)
    
    gamma = math.copysign(abs(beta)+abs(theta), theta)"""
    
    xSquared = length**2+1-2*length*math.cos(math.radians(beta))
    x = math.sqrt(xSquared)
    
    mu = math.copysign(math.degrees(math.asin(math.sin(math.radians(beta))/x)), -beta)
    theta = alpha+mu
    gamma = math.degrees(math.asin((length/x)*math.sin(math.radians(beta))))
    
    print("length:{:.2f}, alpha:{:.2f}, beta:{:.2f} --> x:{:.2f}, mu:{:.2f}, theta:{:.2f}, gamma:{:.2f}\n".format(length, alpha, beta, x, mu, theta, gamma))
    #return x, theta, gamma
    return 0, 0, 0
    
def drive_to_point(x, y, endFacingSameDirection=True):
    theta = math.degrees(math.atan2(y, x))
    length = math.sqrt(x*x+y*y)
    commandList = [CommandTurn(theta), CommandDrive(length)]
    if(endFacingSameDirection):
        commandList.append(CommandTurn(-theta))
    return commandList
    
def drive_to_cube(marker, clearance=1.2):
    alpha = marker.centre.polar.rot_y
    distance = marker.dist-clearance
    distance, alpha, beta = correction2(distance, alpha, 0)
    return [CommandTurn(alpha), CommandDrive(distance)]
    
def align_to_cube(marker, clearance=1):
    alpha = marker.centre.polar.rot_y #angle between camera normal and cube centre
    beta =  marker.orientation.rot_y  #angle between camera cube length and cube normal
    
    length = marker.centre.polar.length #distance between camera and cube
    
    length, alpha, beta = correction2(length, alpha, beta)
    
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
    length0 = length
    alpha0 = math.radians(alpha+OFFSET_ROT_Y)
    beta0 = math.radians(beta)
    x0 = length0*math.sin(alpha0)
    y0 = length0*math.cos(alpha0)
    
    y1 = y0 + OFFSET_Y
    x1 = x0 + OFFSET_X
    
    length1 = math.sqrt(x1*x1 + y1*y1)
    alpha1 = math.asin(x1/length1)
    beta1 = beta0 + alpha0 - alpha1
    
    return length1, math.degrees(alpha1), math.degrees(beta1)
    
def correction2(length, alpha, beta):
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
    

    
    
    
    
    