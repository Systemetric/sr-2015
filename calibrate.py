'''
Calibrating makers.
'''

import json

class CalibrateMarker():
    CALIBRATION_LENGTH = 1.0
    CALIBRATE_FILENAME = "calibration.json"
    
    def __init__(self, robot):
        self.robot = robot
        self.get_marker()
        self.calibrate()
        
    def calibrate(self):
        
        #Get the center of the marker
        #Useful attr's:
        # length - calibrate length to 1m
        # rot_x - calibrate to 0 degrees
        # rot_y - calibrate to 0 degrees
        centre_marker = self.marker.centre.polar
        delta_length = centre_marker.length - CalibrateMarker.CALIBRATION_LENGTH
        delta_rot_x = -centre_marker.rot_x
        delta_rot_y = -centre_marker.rot_y
        json_dict = {"delta_length": delta_length,
                     "delta_rot_x": delta_rot_x,
                     "delta_rot_y": delta_rot_y}
        json_file = open(CalibrateMarker.CALIBRATE_FILENAME, "w")
        json.dump(json_dict, json_file)
    
    def get_marker(self):
        #For calibration, only one marker is expected to be seen. If there are more, you don't know which to calibrate to.
        markers = []
        while len(markers) != 1: 
            markers = self.robot.see()
        self.marker = markers[0]