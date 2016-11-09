import math
from CommandList import *

nets = {'net-a':[0,1,2,3],
        'net-b':[0,2,1,3],
        'net-c':[0,2,3,1]}

class Side() :
    top = 0
    bottom = 1
    front = 2
    right = 3
    back = 4
    left = 5
    wall = 7
    notRecognised = 8
    nope = 9
    
    getName = ["top", "bottom", "front", "right", "back", "left", None, "Wall Marker", "not recognised", "nope"]
    
SIDE_INPUT_TOP = 'Top'
SIDE_INPUT_BOTTOM = 'Bot'
SIDE_INPUT_SIDE_0 = 0
SIDE_INPUT_SIDE_1 = 1
SIDE_INPUT_SIDE_2 = 2
SIDE_INPUT_SIDE_3 = 3
    
def getSideFromMarker(marker):
    """
    This will take a marker and return a side and a net
    """
    pass

    
top = [Side.top, Side.right, Side.bottom, Side.left]
bot = [Side.top, Side.left, Side.bottom, Side.right]

def getOrient(marker,target = 0):
    """
    Returns the side relative to the marker that the target cen be found as a Side enum
    """

    #Read the marker
    if marker == False:
        return None
    n = marker.info.token_net       #read the token marker
    if n == 'NONE':             
        print ('Not a cube')   
    else:
        #If marker found
        if n in nets:
            net = nets[n]
        else:
            print (n)                   #print what net we have found
        

        Cpos = marker.info.code % 100   #mod by 100 to as comp codes are +100
        Cpos -= 32                      #first 32 codes are non token codes (walls etc.)
        Cpos = Cpos % 6                 #mod by 6, to get the side (6 sides hance mod 6 )
        
        #Ajust Cpos to work with code writen
        if Cpos == 0:
            CFace = SIDE_INPUT_TOP               #side 0 is top
            side = False                #not a scoring side
        elif Cpos == 1:                 #side 1 is bottom
            CFace = SIDE_INPUT_BOTTOM
            side = False                #not a scoring side
        else:
            CFace = Cpos - 2            #if not top or bottom -2 so we have sides 0,1,2,3 left (easier to read)
            side = True                 
        
        #If CFace is a side get a CSide from the net index
        if side:
            CSide = net.index(CFace)
            
        #Get the rotation
        rot = marker.orientation.rot_z  #get the rotation of the token
            
        
        #If the side you see is thre same as the target do this
        if CFace == target:
            return Side.front
        
        #If aiming for top or bottom
        if target==SIDE_INPUT_TOP:
            #If target is oposite to visible side
            if CFace==SIDE_INPUT_BOTTOM:
                return Side.back
            if rot < 30 and rot > -30:
                return Side.top
            if rot > 60 and rot < 120:
                return Side.right
            if rot > 150 or rot < -150: 
            	return Side.bottom
            if rot < -60 and rot > -120:
                return Side.left
        elif target==SIDE_INPUT_BOTTOM:
            if CFace==SIDE_INPUT_TOP:
                return Side.back
            if rot < 30 and rot > -30:
                return Side.bottom
            if rot > 60 and rot < 120:
                return Side.left
            if rot > 150 or rot < -150: 
                return Side.top
            if rot < -60 and rot > -120:
                return Side.right
                
        #if aiming for side
        else:
            #Make target net independent
            TSide = net.index(target)        #now that we have 4 sides left, find out where in the net order is the target side (target from srobo libs)
            
            #If the target side is on the opposite side to the one we see
            if side and (CSide - TSide) % 4 == 2: #if we can see a scoring side ('side' = true) and the array indices of the target face and the viewed face are 2 apart 
                return Side.back                  #the number 2 indicates the back facing (opposite way) side
            
            #If target side is to the right of the side we see (visible side facing up)
            if side and (CSide - TSide) % 4 == 1:
                if rot < 30 and rot > -30:
                    return Side.right
                if rot > 60 and rot < 120:
            	    return Side.top
                if rot > 150 or rot < -150: 
            	    return Side.left
                if rot < -60 and rot > -120:
                    return Side.bottom
            
            #If target side is to the left of the side we see (visible side facing up)
            if side and (CSide - TSide) % 4 == 3: #For more detail see https://ninja-prod-uploads.s3.amazonaws.com/54/ca44d0b7af11e58a776b3978f3e0f5/sides.xlsx on someone.io
                if rot < 30 and rot > -30:
                    return Side.left
                if rot > 60 and rot < 120:
            	    return Side.bottom
                if rot > 150 or rot < -150: 
            	    return Side.right
                if rot < -60 and rot > -120:
                    return Side.top
            
            #If top is visible
            if CFace == SIDE_INPUT_TOP:
                if rot < 30 and rot > -30:
            	    return top[(0+TSide)%4]
                if rot > 60 and rot < 120:
            	    return top[(1+TSide)%4]
                if rot > 150 or rot < -150: 
            	    return top[(2+TSide)%4]
                if rot < -60 and rot > -120:
                    return top[(3+TSide)%4]
            
            #if bottom is visible
            if CFace == SIDE_INPUT_BOTTOM:
                if rot < 30 and rot > -30:
            	    return bot[(0+TSide+2)%4]
                if rot > 60 and rot < 120:
            	    return bot[(1+TSide+2)%4]
                if rot > 150 or rot < -150: 
            	    return bot[(2+TSide+2)%4]
                if rot < -60 and rot > -120:
                    return bot[(3+TSide+2)%4]
                    
        return Side.notRecognised    #setup debug alternative
    return Side.nope
    
def output(orient):
    print(Side.getName[orient])
    print(orient)
    
def getRotation(orient,marker,head = True,debug = 0):
    if debug:
        print 'Start get rotation'
    if orient == Side.top:
        if debug: print 'No adjustment'
        if head:
            outStart = [CommandLift(CommandLift.LIFT_HOLDING),CommandSqueeze(False), CommandWrists(CommandWrists.WRISTS_90),CommandLift(CommandLift.LIFT_GROUND),CommandSqueeze(True),CommandLift(CommandLift.LIFT_HOLDING),CommandWrists(CommandWrists.WRISTS_n30),CommandLift(CommandLift.LIFT_HEAD),CommandSuck(True),CommandSqueeze(False)]
            outEnd   = [CommandLift(CommandLift.LIFT_HOLDING),CommandWrists(CommandWrists.WRISTS_n30),CommandLift(CommandLift.LIFT_HEAD),CommandSqueeze(True),CommandSuck(False),CommandLift(CommandLift.LIFT_HOLDING), CommandWrists(CommandWrists.WRISTS_90),CommandLift(CommandLift.LIFT_GROUND),CommandSqueeze(False),CommandLift(CommandLift.LIFT_HOLDING)]
        else:
            outStart = [CommandLift(CommandLift.LIFT_HOLDING),CommandSqueeze(False), CommandWrists(CommandWrists.WRISTS_0), CommandLift(CommandLift.LIFT_GROUND),CommandSqueeze(True),CommandLift(CommandLift.LIFT_HOLDING)]
            outEnd   = [CommandLift(CommandLift.LIFT_GROUND), CommandSqueeze(False), CommandLift(CommandLift.LIFT_HOLDING)]
    elif orient == Side.bottom:
        if debug: print 'a180'
        if head:
            outStart = [CommandLift(CommandLift.LIFT_HOLDING),CommandSqueeze(False), CommandWrists(CommandWrists.WRISTS_90),CommandLift(CommandLift.LIFT_GROUND),CommandSqueeze(True),CommandLift(CommandLift.LIFT_HOLDING),CommandWrists(CommandWrists.WRISTS_n30),CommandLift(CommandLift.LIFT_HEAD),CommandSuck(True),CommandSqueeze(False),CommandLift(CommandLift.LIFT_HOLDING)]
            outEnd   = [CommandLift(CommandLift.LIFT_HOLDING),CommandSqueeze(False), CommandWrists(CommandWrists.WRISTS_n30),CommandLift(CommandLift.LIFT_HEAD),CommandSqueeze(True),CommandSuck(False),CommandLift(CommandLift.LIFT_HOLDING),CommandWrists(CommandWrists.WRISTS_90),CommandLift(CommandLift.LIFT_GROUND),CommandSqueeze(False),CommandLift(CommandLift.LIFT_HOLDING)]
        else:
            outStart = [CommandLift(CommandLift.LIFT_HOLDING),CommandSqueeze(False), CommandWrists(CommandWrists.WRISTS_n90), CommandLift(CommandLift.LIFT_GROUND),CommandSqueeze(True),CommandLift(CommandLift.LIFT_HOLDING),CommandWrists(CommandWrists.WRISTS_90)]
            outEnd   = [CommandLift(CommandLift.LIFT_GROUND), CommandSqueeze(False), CommandLift(CommandLift.LIFT_HEAD)]
    elif orient == Side.front:
        if debug: print 'a090'
        if head:
            outStart = [CommandSqueeze(False), CommandLift(CommandLift.LIFT_GROUND),CommandWrists(CommandWrists.WRISTS_n90),CommandSqueeze(True),CommandLift(CommandLift.LIFT_HOLDING),CommandWrists(CommandWrists.WRISTS_60),CommandLift(CommandLift.LIFT_HEAD),CommandSuck(True),CommandSqueeze(False)]
            outEnd   = [CommandLift(CommandLift.LIFT_HOLDING),CommandWrists(CommandWrists.WRISTS_n30),CommandLift(CommandLift.LIFT_HEAD),CommandSqueeze(True),CommandSuck(False),CommandLift(CommandLift.LIFT_HOLDING), CommandWrists(CommandWrists.WRISTS_90),CommandLift(CommandLift.LIFT_GROUND), CommandSqueeze(False), CommandLift(CommandLift.LIFT_HOLDING)]
        else:
            outStart = [CommandLift(CommandLift.LIFT_HOLDING), CommandSqueeze(False), CommandWrists(CommandWrists.WRISTS_0), CommandLift(CommandLift.LIFT_GROUND),CommandSqueeze(True),CommandLift(CommandLift.LIFT_HOLDING),CommandWrists(CommandWrists.WRISTS_90)]
            outEnd   = [CommandLift(CommandLift.LIFT_GROUND), CommandSqueeze(False), CommandLift(CommandLift.LIFT_HOLDING)]
    elif orient == Side.right:
        if debug: print 't090a090'
        if head:
            top = getOrient(marker, 'Top')
            if top == 0 or top == 1:
                outStart = [CommandLift(CommandLift.LIFT_HOLDING), CommandPlatter(CommandPlatter.PLATTER_0_DEGREES, delay = 0), CommandSqueeze(False), CommandWrists(CommandWrists.WRISTS_90),CommandLift(CommandLift.LIFT_GROUND),CommandSqueeze(True),CommandLift(CommandLift.LIFT_HOLDING),CommandWrists(CommandWrists.WRISTS_n30),CommandLift(CommandLift.LIFT_HEAD),CommandSuck(True),CommandSqueeze(False),CommandLift(CommandLift.LIFT_HOLDING),CommandPlatter(CommandPlatter.PLATTER_90_DEGREES)]
                outEnd   = [CommandWrists(CommandWrists.WRISTS_60),CommandLift(CommandLift.LIFT_HEAD),CommandSqueeze(True),CommandSuck(False),CommandLift(CommandLift.LIFT_HOLDING), CommandWrists(CommandWrists.WRISTS_n90),CommandLift(CommandLift.LIFT_GROUND), CommandSqueeze(False), CommandLift(CommandLift.LIFT_HOLDING)]
            else:
                outStart = [CommandLift(CommandLift.LIFT_HOLDING),CommandSqueeze(False), CommandWrists(CommandWrists.WRISTS_0),CommandLift(CommandLift.LIFT_GROUND),CommandSqueeze(True),CommandLift(CommandLift.LIFT_HOLDING),CommandPlatter(CommandPlatter.PLATTER_0_DEGREES, delay=0),CommandWrists(CommandWrists.WRISTS_n30),CommandLift(CommandLift.LIFT_HEAD),CommandSqueeze(False),CommandLift(CommandLift.LIFT_HOLDING),CommandPlatter(CommandPlatter.PLATTER_90_DEGREES)]
                outEnd   = [CommandLift(CommandLift.LIFT_HOLDING),CommandWrists(CommandWrists.WRISTS_n30),CommandLift(CommandLift.LIFT_HEAD),CommandSqueeze(True),CommandLift(CommandLift.LIFT_HOLDING), CommandWrists(CommandWrists.WRISTS_90),CommandLift(CommandLift.LIFT_GROUND), CommandSqueeze(False), CommandLift(CommandLift.LIFT_HOLDING)]
        else:
            outStart = None
            outEnd   = None
    elif orient == Side.back:
        if debug: print 'a270'
        if head:
            outStart = [CommandLift(CommandLift.LIFT_HOLDING),CommandSqueeze(False), CommandWrists(CommandWrists.WRISTS_0),CommandLift(CommandLift.LIFT_GROUND),CommandSqueeze(True),CommandLift(CommandLift.LIFT_HOLDING),CommandWrists(CommandWrists.WRISTS_n30),CommandLift(CommandLift.LIFT_HEAD),CommandSuck(True),CommandSqueeze(False),CommandLift(CommandLift.LIFT_HOLDING)]
            outEnd   = [CommandLift(CommandLift.LIFT_HOLDING),CommandWrists(CommandWrists.WRISTS_n30),CommandLift(CommandLift.LIFT_HEAD),CommandSqueeze(True),CommandSuck(False),CommandLift(CommandLift.LIFT_HOLDING), CommandWrists(CommandWrists.WRISTS_90),CommandLift(CommandLift.LIFT_GROUND), CommandSqueeze(False), CommandLift(CommandLift.LIFT_HOLDING)]
        else:
            outStart = [CommandLift(CommandLift.LIFT_HOLDING),CommandSqueeze(False), CommandWrists(CommandWrists.WRISTS_0), CommandLift(CommandLift.LIFT_GROUND),CommandSqueeze(True),CommandLift(CommandLift.LIFT_HOLDING),CommandWrists(CommandWrists.WRISTS_n90)]
            outEnd   = [CommandLift(CommandLift.LIFT_GROUND), CommandSqueeze(False), CommandLift(CommandLift.LIFT_HOLDING)]
    elif orient == Side.left:
        if debug: print 't270a090'
        if head:
            top = getOrient(marker, 'Top')
            if top == 0 or top == 1:
                outStart = [CommandLift(CommandLift.LIFT_HOLDING),CommandSqueeze(False), CommandWrists(CommandWrists.WRISTS_90),CommandLift(CommandLift.LIFT_GROUND),CommandSqueeze(True),CommandLift(CommandLift.LIFT_HOLDING),CommandPlatter(CommandPlatter.PLATTER_0_DEGREES),CommandWrists(CommandWrists.WRISTS_n30),CommandLift(CommandLift.LIFT_HEAD),CommandSuck(True),CommandSqueeze(False),CommandLift(CommandLift.LIFT_HOLDING),CommandPlatter(CommandPlatter.PLATTER_270_DEGREES)]
                outEnd   = [CommandLift(CommandLift.LIFT_HOLDING),CommandWrists(CommandWrists.WRISTS_60),CommandLift(CommandLift.LIFT_HEAD),CommandSqueeze(True),CommandSuck(False),CommandLift(CommandLift.LIFT_HOLDING), CommandWrists(CommandWrists.WRISTS_n90),CommandLift(CommandLift.LIFT_GROUND), CommandSqueeze(False), CommandLift(CommandLift.LIFT_HOLDING)]
            else:
                outStart = [CommandLift(CommandLift.LIFT_HOLDING),CommandSqueeze(False), CommandWrists(CommandWrists.WRISTS_0),CommandLift(CommandLift.LIFT_GROUND),CommandSqueeze(True),CommandLift(CommandLift.LIFT_HOLDING),CommandPlatter(CommandPlatter.PLATTER_0_DEGREES),CommandWrists(CommandWrists.WRISTS_n30),CommandLift(CommandLift.LIFT_HEAD),CommandSqueeze(False),CommandLift(CommandLift.LIFT_HOLDING),CommandPlatter(CommandPlatter.PLATTER_270_DEGREES)]
                outEnd   = [CommandLift(CommandLift.LIFT_HOLDING),CommandWrists(CommandWrists.WRISTS_n30),CommandLift(CommandLift.LIFT_HEAD),CommandSqueeze(True),CommandLift(CommandLift.LIFT_HOLDING), CommandWrists(CommandWrists.WRISTS_90),CommandLift(CommandLift.LIFT_GROUND), CommandSqueeze(False), CommandLift(CommandLift.LIFT_HOLDING)]
        else:
            outStart = None
            outEnd   = None
    elif orient == Side.wall:
        if debug: print 'This is a wall/robot/something else marker'
        outStart = None
        outEnd   = None
    else:
        if debug: print 'BROKEN'
        outStart = None
        outEnd   = None
        
    return (outStart,outEnd)