#!/usr/bin/env python

# import module
import sys
sys.path.insert(0, '../')
from base import hooper

def main(): 
    #################################################################################
    #
    target_altitude         = 30000                 
    turn_start_altitude     = 1000                      
    turn_end_altitude       = (target_altitude/1.5)     
    maxq_begin              = 28000
    maxq_end                = 30000
    #
    #################################################################################
    #       X                   Value               Profile                 Weight  #
    #################################################################################
    #
    taxa                    =   0.40                # Hooper              
    #
    #################################################################################

    hooper(turn_start_altitude,turn_end_altitude,target_altitude, maxq_begin, maxq_end, taxa, 180)

main()