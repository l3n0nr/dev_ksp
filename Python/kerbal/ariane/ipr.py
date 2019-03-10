#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import ariane

def main():
    #######################################################################################
    turn_start_altitude     = 2000                      # inclination begin
    turn_end_altitude       = 45000                     # inclination end   
    maxq_begin              = 34000                     # reduce aceleration stage - begin
    maxq_end                = 36000                     # reduce aceleration stage - end    
    #######################################################################################

    orientation             = 90
    target_altitude         = 150000

    ## Interplanetary Relay             -       426 sidereal days
    #       142d        -       2x Probe
    #       142d(284)   -       2x Probe
    #       142d(426)   -       2x Probe

    ariane(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, 1, orientation)

main()