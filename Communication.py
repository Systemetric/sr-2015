''' Communication code in here '''

''' Using code from last year but with commands changed (we know it works) 

Works with the communication code in project 2015-2016 com on roboteam759 mbed account

Mbed communication code- uses mbedlink to send incoming commands to the mbed properly

Provides interface functions:
These control the following commands '>'=recieve '<'=send:
>F[2B]<!<d   drive forwards  [distance in    mm]
>B[2B]<!<d   drive backwards [distance in    mm]

>L[2B]<!<d   turn left       [angle in       degrees]
>R[2B]<!<d   turn right      [angle in       degrees]

>A[1B]<!<l   lift            [0: 0, 1: 42, 2: 120]
>H[1B]<!<w   move wrists     [0: 0, 1: -90, 2: 90, 3:60, 4: -120, 5: -30, 6: U1, 7: U2]

>G[1B]<!<s   squeeze            
>g[1B]<!<s   release         

>T<!         turn Platter continuously
>0<!<p       turn Platter to position 0 (000deg)
>1<!<p       turn Platter to position 1 (090deg)
>2<!<p       turn Platter to position 2 (180deg)
>3<!<p       turn Platter to position 3 (270deg)
>P<!         suck
>p<!         stopSucking

and relays the command & data to the mbed in the correct format
'''



import mbedlink
import struct
import math

#Helper functions for processing command input and output data-------------------------------------------------------------------------------------------------
def inputByte(data):
    #if data<128 and data>=-128:
    #    return chr(data)
    return struct.pack('>b', data)

def inputShort(data):
    return struct.pack('>h', data)
    
def inputU2B(data):#unsigned 2 bytes
    return struct.pack('>H', data)
    
def inputU1B(data):#unsigned 1 bytes
    return struct.pack('>B', data)
    
def outputTemp(data):
    print "REPLYFUNC: %s" %str(data)
    return data

def outputDataTemp(data):
    print "Cmd back: %s" %data[0]
    print "Data back: %s" %struct.unpack('>h', data[1:])
    
def replyFunc2(data):
    print "response2: %s" %str(data)
    
#Link to the mbed
mbed = mbedlink.Mbed('/dev/ttyACM0')

#Commands we plan to use go here----------------------------------------------------------------------------------------------------------------------------------
commandMoveForward =    mbedlink.MbedCommand('F', 2, 1, inputfunc=inputU2B, replyfunc=outputTemp, responselength2=1, replyfunc2=replyFunc2)
commandMoveBackwards =  mbedlink.MbedCommand('B', 2, 1, inputfunc=inputU2B, replyfunc=outputTemp, responselength2=1, replyfunc2=replyFunc2)

commandTurnLeft =       mbedlink.MbedCommand('L', 2, 1, inputfunc=inputU2B, replyfunc=outputTemp, responselength2=1, replyfunc2=replyFunc2)
commandTurnRight =      mbedlink.MbedCommand('R', 2, 1, inputfunc=inputU2B, replyfunc=outputTemp, responselength2=1, replyfunc2=replyFunc2)

commandMoveArms =       mbedlink.MbedCommand('A', 1, 1, inputfunc=inputU1B, replyfunc=outputTemp, responselength2=1, replyfunc2=replyFunc2)
commandMoveWrists =      mbedlink.MbedCommand('H', 1, 1, inputfunc=inputU1B, replyfunc=outputTemp, responselength2=1, replyfunc2=replyFunc2)

commandSqueeze =           mbedlink.MbedCommand('G', 0, 1, replyfunc=outputTemp, responselength2=1, replyfunc2=replyFunc2)
commandRelease =        mbedlink.MbedCommand('g', 0, 1, replyfunc=outputTemp, responselength2=1, replyfunc2=replyFunc2)
    
commandPlatterCR =    mbedlink.MbedCommand('T', 0, 1, replyfunc=outputTemp)
commandPlatter0 =     mbedlink.MbedCommand('0', 0, 1, replyfunc=outputTemp, responselength2=1, replyfunc2=replyFunc2)
commandPlatter1 =     mbedlink.MbedCommand('1', 0, 1, replyfunc=outputTemp, responselength2=1, replyfunc2=replyFunc2)
commandPlatter2 =     mbedlink.MbedCommand('2', 0, 1, replyfunc=outputTemp, responselength2=1, replyfunc2=replyFunc2)
commandPlatter3 =     mbedlink.MbedCommand('3', 0, 1, replyfunc=outputTemp, responselength2=1, replyfunc2=replyFunc2)
commandSuck =           mbedlink.MbedCommand('P', 0, 1, replyfunc=outputTemp)#no second response
commandStopSucking =    mbedlink.MbedCommand('p', 0, 1, replyfunc=outputTemp)#no second response

"""Old commands saved as examples"""
"""commandMove = mbedlink.MbedCommand(     'M', 2, 3, inputfunc=inputShort, replyfunc=outputDataTemp, responselength2=1, replyfunc2=replyFunc2)
commandTurn = mbedlink.MbedCommand(     'T', 2, 3, inputfunc=inputShort, replyfunc=outputDataTemp, responselength2=1, replyfunc2=replyFunc2)
commandData = mbedlink.MbedCommand(     'D', 0, 1, replyfunc=outputTemp)#Unknown params
commandMoveArms = mbedlink.MbedCommand( 'A', 2, 3, inputfunc = inputShort, replyfunc = outputDataTemp, responselength2 = 1, replyfunc2= replyFunc2)
commandGrab = mbedlink.MbedCommand(     'G', 1, 1, inputfunc = inputByte, replyfunc = outputTemp)
commandSuck = mbedlink.MbedCommand(     'S', 1, 1, inputfunc = inputByte, replyfunc = outputTemp)
commandMoveHands = mbedlink.MbedCommand('H', 2, 3, inputfunc = inputShort, replyfunc = outputDataTemp, responselength2 = 1, replyfunc2= replyFunc2)"""

#Interface functions - allow sending of mbed commands from other code------------------------------------------------------------------------------------------------
#Whenever you make a new mbedcommand, define the function to send it here

def drive(distance):
    print('Drive : {} m'.format(distance))
    command=None
    if(distance>0):
        command=commandMoveForward
    elif(distance<0):
        command=commandMoveBackwards
    else:
        print("Cannot move 0m")
        return None
    mbed.send(command, abs(int(distance*1000)))
    
def turn(angle):
    print('Turn : %d degrees' %(angle))
    if abs(angle) < 1:
        print ('Not actually turning')
    else:
        command=None
        if(angle>0):
            command=commandTurnRight
        elif(angle<0):
            command=commandTurnLeft
        mbed.send(command, abs(angle))

PLATTER_0_DEGREES = 0
PLATTER_90_DEGREES = 1
PLATTER_180_DEGREES = 2
PLATTER_270_DEGREES = 3
PLATTER_CONTINUOUS = 4
def movePlatter(mode):
    """modes:   0 don't move
                1  90 deg
                2 180 deg
                3 270 deg
                4 continuously"""
    print('Turning Platter mode {}'.format(mode))
    if(mode==0):
        mbed.send(commandPlatter0)
    elif(mode==1):
        mbed.send(commandPlatter1)
    elif(mode==2):
        mbed.send(commandPlatter2)
    elif(mode==3):
        mbed.send(commandPlatter3)
    elif(mode==4):
        mbed.send(commandPlatterCR)

def squeezeArms(enable):
    if enable:
        print("Grabbing")
        mbed.send(commandSqueeze)
    else:
        print("Releasing")
        mbed.send(commandRelease)
         
LIFT_GROUND = 0
LIFT_HOLDING = 1
LIFT_HEAD = 2
def liftArms(angle):
    print('Lifting Arms to Angle: %d degrees' %(angle))
    mbed.send(commandMoveArms, angle)

#Relative to the arms
WRISTS_0 = 0
WRISTS_n90 = 1
WRISTS_90 = 2
WRISTS_60 = 3
WRISTS_n120 = 4
WRISTS_n30 = 5
WRISTS_unknown1 = 6
WRISTS_unknown2 = 7
def moveWrists(angle):
    print('Turning Wrists to angle: %d degrees' %(angle))
    mbed.send(commandMoveWrists, angle)
   
def suck(enable):
    print('Setting sucker to %s' %(enable))
    if enable:
        mbed.send(commandSuck)
    else:
        mbed.send(commandStopSucking)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    