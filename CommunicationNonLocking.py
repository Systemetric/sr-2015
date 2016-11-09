'''
Non locking locking implementation of the mbed comms
'''
''' Communication code in here '''

''' Using code from last year but with commands changed (we know it works) 

Works with the communication code in project 2015-2016 com on roboteam759 mbed account

Mbed communication code- uses mbedlink to send incoming commands to the mbed properly

Provides interface functions:
drive     in m
turn      in degrees (right+,left-)
moveArms  in degrees
grab      as bool (0 or 1)
suck      as bool (0 or 1)

These control the following commands '>'=send '<'=recieve:
>F[2B]<!<d   drive forwards  [distance in    mm]
>B[2B]<!<d   drive backwards [distance in    mm]

>L[2B]<!<d   turn left       [angle in       degrees]
>R[2B]<!<d   turn right      [angle in       degrees]

>A[1B]<!<d   move arms       [code for arm position (to be defined)]
>H[1B]<!<d   move hands      [code for hand position (to be defined)]
>G[1B]<!     grab            [bool (0 or 1)]

>T<!         turn turntable continuously
>0<!         turn turntable to position 0 (000deg)
>1<!         turn turntable to position 1 (090deg)
>2<!         turn turntable to position 2 (180deg)
>3<!         turn turntable to position 3 (270deg)
>S[1B]<!     suck            [bool (0 or 1)]

and relays the command & data to the mbed in the correct format
'''



import mbedlink2 as mbedlink
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
    
def inputS2B(data):#signed 2 bytes
    return struct.pack('>h', data)
    
def inputU1B(data):#unsigned 1 byte
    return struct.pack('>B', data)
    
def inputS1B(data):#signed 1 byte
    return struct.pack('>b', data)
    
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
commandDrive        =       mbedlink.MbedCommand('D', 2, 1, inputfunc=inputS2B, replyfunc=outputTemp, responselength2=1, replyfunc2=replyFunc2)
commandMoveArms     =       mbedlink.MbedCommand('A', 1, 0, inputfunc=inputU1B, replyfunc=outputTemp)
commandTurn         =       mbedlink.MbedCommand('R', 1, 1, inputfunc=inputS1B, replyfunc=outputTemp)
commandTurnTable    =       mbedlink.MbedCommand('T', 1, 0, inputfunc=inputU1B, replyfunc=outputTemp)
commandMoveHands    =       mbedlink.MbedCommand('H', 1, 0, inputfunc=inputU1B, replyfunc=outputTemp)

commandGrab         =       mbedlink.MbedCommand('G', 1, 0, inputfunc=inputU1B, replyfunc=outputTemp)#no second response
commandSuck         =       mbedlink.MbedCommand('S', 1, 1, inputfunc=inputU1B, replyfunc=outputTemp, responselength2=1, replyfunc2=replyFunc2)#no second response

#Interface functions - allow sending of mbed commands from other code------------------------------------------------------------------------------------------------
#Whenever you make a new mbedcommand, define the function to send it here

def drive(distanceLeft,distanceRight):
    print('Drive : {0}{1} m'.format(distanceLeft,distanceRight))
    command=commandDrive
    if(distanceLeft == 0 and distanceRight == 0):
        print("Cannot move 0m")
        return None
    #mbed.send(command, int(distanceLeft) OPP for single arg int(distanceRight))
    
def turn(angle):
    print('Turn : %d degrees' %(angle))
    if abs(angle) < 5:
        print ('Not actually turning')
    else:
        mbed.send(commandTurn, int(angle))
        
def moveTurnTable(mode):
    """modes:   0 don't move
                1  90 deg
                2 180 deg
                3 270 deg
                4 continuously"""
    print('Turning Table mode {}'.format(mode))
    #mbed.send()
    
#THE FOLLOWING FUNCTIONS ARE NOT FINALIZED OR FINISHED------------------------------------------------------------------------------------------------------------------        
def moveArms(angle):
    print('Turning Arms to Angle: %d degrees' %(angle))
    mbed.send(commandMoveArms, angle)
    
def moveHands(angle):
    print('Turning Hands to angle: %d degrees' %(angle))
    mbed.send(commandMoveHands, angle)

def grab(grabbing):
    print('Setting grabber to %s' %(grabbing))
    mbed.send(commandGrab, grabbing)

def suck(on):
    print('Setting sucker to %s' %(on))
    mbed.send(commandSuck, on)