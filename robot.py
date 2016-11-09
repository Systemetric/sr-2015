from sr.robot import *
#from Hobo import *
from Tobo import *
import time
import Communication as movement

"""
Moved all of the test functions to Tobo
This is a class that extends sr.robot.Robot
If you want to add a test funtion add it to Tobo
If you want to add a final code function add it to Hobo
Change the main function to switch programs
"""
if __name__ == "__main__":
    robot = Tobo()
    print('Finish init, start code')
    #robot.move_to_cube()
    #robot.turn_back()
    #robot.move_square()
    #movement.drive(1)
    
    #robot.move_to_cube_improved()
    #robot.move_snake()
    #robot.camera_error_calibration()
    #robot.move_m(1)
    #robot.new_alignment_test()
    #robot.arms_test()
    
    #robot.warm_up_wrists()
    
    #robot.alignment_test()
    #robot.solving_test()
    #robot.test_return()
    #robot.test_decision()
    #robot.run_commands([CommandPlatter(4)])
    #robot.full_drive_to_cube()
    
    robot.initialize()
    robot.startComp2()
    
    #robot.run_commands([CommandWrists(CommandWrists.WRISTS_n120), CommandWrists(CommandWrists.WRISTS_90),CommandWrists(CommandWrists.WRISTS_0)])
    
    #robot.run_commands([CommandSqueeze(False)])
    #robot.panicComp()
    #robot.do_everything()
    
    '''
    while 0:
        m=robot.see()
        while len(m)>0:
            face = robot.marker_orientation(m[0])
            #print(robot.marker_rotation(face))
            time.sleep(1)
            #if face <> 0:
            robot.move_to_cube(m[0])
            print(robot.marker_rotation(face))
            time.sleep(10)
            break
            #else:
               # m.pop(0)
        time.sleep(.1)'''
