''' This file is for working out where in the arena you are if you can see a wall marker '''
import math
from sr.robot import *

class placement:
    code = 0
    side = 0
    marker_x = 0
    marker_y = 0
    adjust_x = 0
    adjust_y = 0
    polar_y = 0
    
class zones:
    # These reprent the zones as defined in the rules
    Corner0 = 0
    Corner1 = 1
    Corner2 = 2
    Corner3 = 3
    Centre  = 4
    Invalid = 5
    

def get_placement(m):
    temp = placement()
    
    side = m.info.code / 7
    mPos = -4 + (m.code % 7) +1
    
    temp.polar_y = m.rot_y
    temp.side = side
    temp.code = m.info.code
    
    ''' Calculating the position of the marker '''
    if side == 0:
        temp.x = mPos
        temp.y = 4
    if side == 1:
        temp.x = 4
        temp.y = -mPos
    if side == 2:
        temp.x = -mPos
        temp.y = -4
    if side == 3:
        temp.x = -4
        temp.y = mPos
    
    ''' Calculates position of robot relative to marker ''' 
    if side == 0:
        # It is the top
        x = m.dist * math.sin(math.radians(m.orientation.rot_y)) * -1
        y = m.dist * math.cos(math.radians(m.orientation.rot_y)) * -1 
    if side == 1:
        # It is the right
        x = m.dist * math.cos(math.radians(m.orientation.rot_y)) * -1
        y = m.dist * math.sin(math.radians(m.orientation.rot_y))
    if side == 2:
        # It is the bottom
        x = m.dist * math.sin(math.radians(m.orientation.rot_y))
        y = m.dist * math.cos(math.radians(m.orientation.rot_y))
    if side == 3:
        # It is the left
        x = m.dist * math.cos(math.radians(m.orientation.rot_y)) 
        y = m.dist * math.sin(math.radians(m.orientation.rot_y)) * -1
        
    return temp
    

def find_position(R):
    ''' 
    This takes in a robot and looks for markers. It returns None if no 
    markers seen or the average coordinates as calculated by the markers 
    in a tuple (x,y)         
    '''
    seen = R.see()
    markers = []
    
    for m in seen:
        if m.info.marker_type == MARKER_ARENA:
            # Get the placement information 
            temp = get_placement(m)
            # Append to the list of markers 
            markers.append(temp)
            
        if len(markers) == 0:
            return None
        
        else:
            count = 0
            position = (0,0)
            
            for m in markers:
                newPos = (m.marker_x + m.adjust_x,m.marker_y+m.adjust_y)
                position = (position[0]*count + newPos[0], position[1]*count + newPos[1])
                count += 1
                position = (position[0]/count,position[1]/count)
                
            return position
            
def find_zone (coordinates):
    ''' 
    This takes in a tuple of coordinates (x,y) and returns 
    the zone those coordinates are located in 
    '''       
    
    # Store original quadrant
    x_sign = coordinates[0] / abs(coordinates[0])
    y_sign = coordinates[1] / abs(coordinates[1])
    
    # Convert to being in the upper left quadrant
    coordinates = (abs(coordinates[0]),abs(coordinates[1]))
    if (coordinates[1] > 4) or (coordinates[0] > 4):
        # Then this point is outside the arena
        return zones.Invalid
    elif coordinates[1] < (6 - coordinates[0]):
        # Then you are in the centre zone
        return zones.Centre
    else:
        # You are in a corner zone
        if (x_sign == 1) and (y_sign == 1):
            #You are in corner 1
            return zones.Corner1
        if (x_sign == 1) and (y_sign == -1):
            #You are in corner 2
            return zones.Corner2
        if (x_sign == -1) and (y_sign == -1):
            #You are in corner 3
            return zones.Corner3
        if (x_sign == -1) and (y_sign == 1):
            #You are in corner 0
            return zones.Corner0
            
def check_home_zone(R):
    ''' 
    This looks for markers to confirm you are in your home zone. 
    It takes in a robot and returns none if it cant see any markers
    and returns true or false if it can.
    '''
    
    robot_position = find_position(R)
    if robot_position == None:
        return None
    else:
        zone = find_zone(robot_position)
    
        if zone == R.zone:
            return True
        else:
            return False
            
def check_home_offset(R,offset,angle = 0):
    '''
    Checks whether a point 'offset' meters ahead when the 
    robot has turned though 'angle' degrees is in the 
    home zone of the robot.
    It has the same outputs as check_home_zone
    '''
    
    robot_position = find_position(R)
    if robot_position == None:
        return None
    else:
        angle = angle + R.currentAngle
        
        direction = angle / 90
        angle = math.radians(angle % 90)
        
        if direction == 0:
            adjust_x = offset * math.sin(angle)
            adjust_y = offset * math.cos(angle)
        if direction == 1:
            adjust_x = offset * math.cos(angle)
            adjust_y = offset * math.sin(angle) * -1
        if direction == 2:
            adjust_x = offset * math.sin(angle) * -1
            adjust_y = offset * math.cos(angle) * -1
        if direction == 3:
            adjust_x = offset * math.sin(angle) * -1
            adjust_y = offset * math.cos(angle)
        
        offset_position = (robot_position[0]+adjust_x,robot_position[1]+adjust_y)
        
        zone = find_zone(offset_position)
    
        if zone == R.zone:
            return True
        else:
            return False
            
def find_angle(R):
    '''
    This uses wall markers to find the angle the robot is at relative to the arena
    with 0 degrees being pointing to the wall with corners 0 & 1
    It takes in a robot and outputs an angle in degrees or None if it cannot see
    any markers
    '''
        
    robot_position = find_position(R)
    seen = R.see()
    markers = []
    
    for m in seen:
        if m.info.marker_type == MARKER_ARENA:
            temp = get_placement(m)
            markers.append(temp)
            
    angle = 0
    count = 0
    
    # not tested, 90% sure it is wrong
    for m in markers:
        if m.side == 0:
            newAngle = -math.degrees(math.atan(m.adjust_x/m.adjust_y))
        if m.side == 1:
            newAngle = math.degrees(math.atan(m.adjust_y/m.adjust_x))
        if m.side == 2:
            newAngle = -math.degrees(math.atan(m.adjust_x/m.adjust_y))
        if m.side == 3:
            newAngle = math.degrees(math.atan(m.adjust_y/m.adjust_x))
            
        angle = angle*count + newAngle
        count += 1
        angle = angle/count
        
    return angle
    
    
        
        
        
    