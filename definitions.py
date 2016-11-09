#Definitions
WRISTS_0         =  0x1F
WRISTS_n90       =  0x3F
WRISTS_90       =   0x5F
WRISTS_60        =  0x7F
WRISTS_n120       = 0x9F
WRISTS_n30        = 0xBF
WRISTS_unknown1    =0xDF
WRISTS_unknown2 =   0xFF

PLATTER_0  =         0xF8
PLATTER_90  =        0xF9
PLATTER_180  =       0xFA
PLATTER_270   =      0xFB
PLATTER_CR     =     0xFC

LIFT_0          =    0xE7
LIFT_42          =   0xE8
LIFT_120          =  0xE9

SQUEEZE_IN  =  0
SQUEEZE_OUT  =  1

oneDegree = (2500.0/90.0)#was 2650.0-->2026
oneMM = (2650.0/325.0)
stepTime = 0.0003
#2650 steps gives 180 degrees and 650mm straight line
#2650 steps now gives 90 degrees and 325mm straight line

START_STEPS_PER_SECOND = 1000
MAX_STEPS_PER_SECOND = 9000
FINISH_STEPS_PER_SECOND = 1000

STEPS_PER_SECOND_PER_SECOND = 500
STEPS_TO_INCREMENT =  2

STEPS_TO_ACCELERATE =(MAX_STEPS_PER_SECOND * MAX_STEPS_PER_SECOND - START_STEPS_PER_SECOND * START_STEPS_PER_SECOND) / (2 * STEPS_TO_INCREMENT * STEPS_PER_SECOND_PER_SECOND)
STEPS_TO_DECCELERATE =(MAX_STEPS_PER_SECOND * MAX_STEPS_PER_SECOND - FINISH_STEPS_PER_SECOND * FINISH_STEPS_PER_SECOND) / (2 * STEPS_TO_INCREMENT * STEPS_PER_SECOND_PER_SECOND)

TIME_BETWEEN_INCREMENTS = 1000000/STEPS_PER_SECOND_PER_SECOND
'''
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
'''