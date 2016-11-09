import time
import Communication as movement


class Command():
    """Virtual class"""
    def __init__(self):
        pass

class CommandDrive(Command):
    def __init__(self, distance, delay=.5):
        self.distance = distance
        self.delay = delay
        
    def run(self):
        print("Driving {} meters".format(self.distance))
        movement.drive(self.distance)
        time.sleep(self.delay)
        
class CommandTurn(Command):
    def __init__(self, angle, delay=.5):
        self.angle = angle
        self.delay = delay
        
    def run(self):
        print("Turning {} degrees".format(self.angle))
        movement.turn(self.angle)
        time.sleep(self.delay)
        
class CommandSqueeze(Command):
    def __init__(self, enable, delay=.1):
        self.enable = enable
        self.delay = delay
        
    def run(self):
        print("Setting Arms Grab to {}".format(self.enable))
        movement.squeezeArms(self.enable)
        time.sleep(self.delay)
        
class CommandLift(Command):
    
    LIFT_GROUND = 0
    LIFT_HOLDING = 1
    LIFT_HEAD = 2
    
    def __init__(self, position, delay=3):
        self.position = position
        self.delay = delay
        
    def run(self):
        print("Lifting Arms to {}".format(self.position))
        movement.liftArms(self.position)
        time.sleep(self.delay)
        
class CommandWrists(Command):
    
    WRISTS_0 = 0
    WRISTS_n90 = 1
    WRISTS_90 = 2
    WRISTS_60 = 3
    WRISTS_n120 = 4
    WRISTS_n30 = 5
    WRISTS_unknown1 = 6
    WRISTS_unknown2 = 7
    
    def __init__(self, position, delay=.1):
        self.position = position
        self.delay = delay
        
    def run(self):
        print("Moving Writsts to {}".format(self.position))
        movement.moveWrists(self.position)
        time.sleep(self.delay)
        
class CommandPlatter(Command):
    
    PLATTER_0_DEGREES = 0
    PLATTER_90_DEGREES = 1
    PLATTER_180_DEGREES = 2
    PLATTER_270_DEGREES = 3
    PLATTER_CONTINUOUS = 4
    
    def __init__(self, position, delay=.5):
        self.position = position
        self.delay = delay
        
    def run(self):
        print("Turning platter {}".format(self.position))
        movement.movePlatter(self.position)
        time.sleep(self.delay)
        
class CommandSuck(Command):
    SUCK_ENABLE = True
    SUCK_DISABLE = False
    
    def __init__(self, enable, delay=.5):
        self.enable = enable
        self.delay = delay
        
    def run(self):
        if self.enable:
            print "Suck activating"
        else:
            print "Suck deactivating"
        movement.suck(self.enable)
                