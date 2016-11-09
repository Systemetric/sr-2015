'''
Used by Communication to send stuff to the mbed properly 

This has been directly copied from Aluminati's Code
Correctly formats mbed commands and sends them over the serial connection
'''

import serial
import sys
import threading
import time

class MbedCommand:
    """A type of command to send to the MBED"""

    def __init__(self, char, datalength=0, responselength=1, inputfunc=None, replyfunc=None, responselength2=0, replyfunc2=None, timeout2=30):
        """
        char:           Command character
        datalength:     Length of data to send to MBED (chars/bytes)
        responselength: Length of data to get back (chars/bytes)
        inputfunc:      Function to validate/preprocess data before sending
        replyfunc:      Function to process response data
        responseLength2:Length of data to get back of second response from mbed
        replyFunc2:     Function to process 2nd response data
        """
        
        self.char = char
        self.datalength = datalength
        self.responselength = responselength
        self.responselength2 = responselength2
        self.timeout2 = timeout2

        if inputfunc: self.inputfunc = inputfunc
        else:         self.inputfunc = lambda s: str(s)

        if replyfunc: self.replyfunc = replyfunc
        else:         self.replyfunc = lambda s: s
        
        if replyfunc2: self.replyfunc2 = replyfunc2
        else:          self.replyfunc2 = lambda s: s

# Dummy command. MBED responds somehow, unless it doesn't anymore.
dummycommand = MbedCommand('d', datalength=1, responselength=1)

class Mbed(object):
    """Serial connection to MBED"""
    __usedports = set()
    __usedportslock = threading.Lock()

    # Char to preface commands with
    __START_CHAR = 's'
    # Char used by MBED to signify error
    __ERROR_CHAR = '?'

    def __init__(self, port, timeout=0.2):
        self.defaultTimeout = timeout
        self.state = 'failed'
        self.__sendlock = threading.Lock()
        with Mbed.__usedportslock:
            if port in Mbed.__usedports:
                print "Another instance using this port!"
            Mbed.__usedports.add(port)

        #Connect to MBED on port
        try:
            with self.__sendlock:
                self.mbed = serial.Serial(port, timeout=timeout, writeTimeout=timeout)
                #self.mbed.open() # MBED seems to open this.
                # Handshaking?
                #if self.mbed.read(1) == 'h':
                self.state = 'working'
                #else: print "Wrong/no MBED handshake"
        except:
            print "Connecting to MBED on %s failed!" %port


    def send(self, command, data=''):
        """
        Send command with data
        Returns command.responselength bytes on success,
        False on error response, None if no or invalid response.
        """
        
        assert(self.state == 'working')

        data = command.inputfunc(data)
        
        if len(data) != command.datalength:
            raise AssertionError("Invalid data length for command %s"%command.char) 
        
        outstring = Mbed.__START_CHAR + command.char + data
        #make sure we don't try to send two commands at the same time by locking
        with self.__sendlock:
            try:
                self.mbed.write(outstring)
            except serial.SerialTimeoutException:
                print "Timeout sending", outstring
                return None
            response = self.mbed.read(command.responselength)
            time.sleep(0.01) # Wait in case unexpected extra chars show up
            if self.mbed.inWaiting():
                print "Received overlong response to command %s of %s" %(outstring, response)
            self.mbed.flushInput()

        if not response:
            print "No response to command", outstring
            return None
        elif response == Mbed.__ERROR_CHAR:
            print "Mbed replied with error to", outstring
            return False
        elif len(response) != command.responselength:
            print "Only got %d chars, not %d for command %s" %(len(response), command.responselength, outstring)
            return None
        #handle the 2nd response if one is expected
        if command.responselength2:
            with self.__sendlock:
                self.mbed.timeout = command.timeout2
                response2 = self.mbed.read(command.responselength2)
                time.sleep(0.01)
                if self.mbed.inWaiting():
                    print "Received overlong response2 to command %s" %outstring
                self.mbed.flushInput()
                self.mbed.timeout = self.defaultTimeout
                
                if not response2:
                    print "No response2 to command", outstring
                    return None
                elif response2 == Mbed.__ERROR_CHAR:
                    print "Mbed replied (2) with error to", outstring
                    return False
                elif len(response2) != command.responselength2:
                    print "Only got %d chars (2), not %d for command %s" %(len(response2), command.responselength2, outstring)
                    return None
                
            return (command.replyfunc(response), command.replyfunc2(response2))
            
        return command.replyfunc(response)